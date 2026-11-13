
import streamlit as st
import pandas as pd

from database import create_tables, get_connection
from seed_data import insert_dummy_records
from pensioner_service import get_pensioner_by_ppo, get_all_pensioners
from verification_service import verify_certificate
from certificate_service import get_certificate_history, get_all_certificates
from gemini_service import explain_rejection, generate_pension_guidance
from notification_service import (
    generate_whatsapp_message,
    generate_success_message
)
from email_service import send_pension_email


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Life Certificate Assistance",
    page_icon="📄",
    layout="wide"
)

create_tables()

st.title("AI Life Certificate Assistance System")

st.caption(
    "Educational demo: Streamlit + SQLite + Google Gen AI SDK"
)

st.warning(
    "This is not an official government or bank portal. "
    "Local demo verification is not official pension approval."
)


# --------------------------------------------------
# SIDEBAR MENU
# --------------------------------------------------

menu = st.sidebar.radio(
    "Choose an operation",
    [
        "Dashboard",
        "Submit / Resubmit Certificate",
        "AI Rejection Explanation",
        "AI Pension Chatbot",
        "Certificate History",
        "Pensioner Records"
    ]
)


# ==================================================
# 1. DASHBOARD
# ==================================================

if menu == "Dashboard":

    st.subheader("Application Dashboard")

    connection = get_connection()

    pensioners_df = pd.read_sql_query(
        "SELECT * FROM pensioners",
        connection
    )

    certificates_df = pd.read_sql_query(
        "SELECT * FROM life_certificates",
        connection
    )

    connection.close()

    total_pensioners = len(pensioners_df)
    total_submissions = len(certificates_df)

    approved = 0
    rejected = 0

    if not certificates_df.empty:

        approved = int(
            (certificates_df["status"] == "APPROVED").sum()
        )

        rejected = int(
            (certificates_df["status"] == "REJECTED").sum()
        )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Pensioners", total_pensioners)
    c2.metric("Submissions", total_submissions)
    c3.metric("Demo approved", approved)
    c4.metric("Rejected", rejected)

    st.subheader("Recent submissions")

    if certificates_df.empty:

        st.info("No submissions have been recorded yet.")

    else:

        st.dataframe(
            certificates_df.tail(10),
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# 2. SUBMIT / RESUBMIT LIFE CERTIFICATE
# ==================================================

elif menu == "Submit / Resubmit Certificate":

    st.subheader("Find registered pensioner")

    ppo_lookup = st.text_input(
        "Registered PPO number"
    )

    if st.button("Find pensioner"):

        person = get_pensioner_by_ppo(ppo_lookup)

        if person:

            st.session_state["selected_pensioner"] = person

            st.session_state.pop("last_result", None)
            st.session_state.pop("last_person", None)

            st.success("Demo pensioner record found.")

        else:

            st.session_state.pop("selected_pensioner", None)
            st.session_state.pop("last_result", None)
            st.session_state.pop("last_person", None)

            st.error("No matching demo record was found.")

    # Retrieve selected pensioner

    person = st.session_state.get("selected_pensioner")

    if person:

        st.write("Pensioner:", person["name"])
        st.write("Registered PPO:", person["ppo_number"])
        st.write("Bank:", person["bank_name"])
        st.write("Registered IFSC:", person["ifsc"])

        # ------------------------------------------
        # LIFE CERTIFICATE FORM
        # ------------------------------------------

        with st.form("life_certificate_form"):

            entered_ppo = st.text_input(
                "PPO number to submit",
                value=person["ppo_number"]
            )

            entered_account = st.text_input(
                "Bank account number",
                value=person["account_number"]
            )

            entered_ifsc = st.text_input(
                "IFSC code",
                value=person["ifsc"]
            )

            submitted = st.form_submit_button(
                "Submit/Resubmit Life Certificate"
            )

        # ------------------------------------------
        # PROCESS FORM SUBMISSION
        # ------------------------------------------

        if submitted:

            st.session_state.pop("last_result", None)
            st.session_state.pop("last_person", None)

            if not entered_ppo.strip():

                st.error("PPO number is required.")

            elif not entered_account.strip():

                st.error("Bank account number is required.")

            elif not entered_ifsc.strip():

                st.error("IFSC code is required.")

            else:

                result = verify_certificate(
                    person,
                    entered_ppo,
                    entered_account,
                    entered_ifsc
                )

                st.session_state["last_result"] = result

                st.session_state["last_person"] = person

        # ------------------------------------------
        # DISPLAY VERIFICATION RESULT
        # ------------------------------------------

        result = st.session_state.get("last_result")

        result_person = st.session_state.get("last_person")

        if result and result_person:

            if result["status"] == "REJECTED":

                st.error(
                    "Submission rejected by demo rules."
                )

                st.write(
                    "Reason:",
                    result["reason"]
                )

                # WHATSAPP MESSAGE PREVIEW

                wa_text = generate_whatsapp_message(
                    result_person["name"],
                    result["certificate_id"],
                    result["reason"]
                )

                st.subheader("WhatsApp message preview")

                st.code(wa_text)

                # ----------------------------------
                # EMAIL NOTIFICATION
                # ----------------------------------

                st.subheader("Send rejection email")

                st.write(
                    "Send an email notification to the "
                    "registered pensioner."
                )

                # IMPORTANT: EMAIL BUTTON IS OUTSIDE THE FORM

                if st.button("Send email notification"):

                    receiver_email = (
                        result_person.get("email") or ""
                    ).strip()

                    if not receiver_email:

                        st.error(
                            "Pensioner's email address is missing."
                        )

                    else:

                        ok, message = send_pension_email(
                            receiver_email,
                            result_person["name"],
                            result["certificate_id"],
                            result["reason"]
                        )

                        if ok:

                            st.success(message)

                        else:

                            st.error(message)

            else:

                st.success(
                    "Local demo checks passed."
                )

                st.info(
                    generate_success_message(
                        result_person["name"],
                        result["certificate_id"]
                    )
                )


# ==================================================
# 3. AI REJECTION EXPLANATION
# ==================================================

elif menu == "AI Rejection Explanation":

    st.subheader(
        "Explain rejection with Google Gemini"
    )

    result = st.session_state.get("last_result")

    person = st.session_state.get("last_person")

    if result and person and result["status"] == "REJECTED":

        st.write(
            "Pensioner:",
            person["name"]
        )

        st.write(
            "Rejection reason:",
            result["reason"]
        )

        if st.button("Generate AI explanation"):

            with st.spinner(
                "Gemini is preparing an explanation..."
            ):

                try:

                    answer = explain_rejection(
                        person["name"],
                        result["reason"]
                    )

                    st.markdown(answer)

                except Exception as error:

                    st.error(
                        f"Gemini request failed: {error}"
                    )

    else:

        st.info(
            "First submit a certificate that is rejected "
            "by the demo verification rules."
        )


# ==================================================
# 4. AI PENSION CHATBOT
# ==================================================

elif menu == "AI Pension Chatbot":

    st.subheader(
        "Ask the AI pension assistance guide"
    )

    question = st.text_area(
        "Enter a general question about Life Certificates"
    )

    if st.button("Ask Gemini"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner("Waiting for Gemini..."):

                try:

                    response = generate_pension_guidance(
                        question
                    )

                    st.markdown(response)

                except Exception as error:

                    st.error(
                        f"Gemini request failed: {error}"
                    )


# ==================================================
# 5. CERTIFICATE HISTORY
# ==================================================

elif menu == "Certificate History":

    st.subheader("Search submission history")

    history_ppo = st.text_input(
        "Registered PPO number"
    )

    if st.button("View certificate history"):

        person = get_pensioner_by_ppo(history_ppo)

        if not person:

            st.error("Pensioner not found.")

        else:

            records = get_certificate_history(
                person["pensioner_id"]
            )

            if records:

                st.dataframe(
                    pd.DataFrame(records),
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No submission history exists."
                )


# ==================================================
# 6. PENSIONER RECORDS
# ==================================================

elif menu == "Pensioner Records":

    st.subheader(
        "Registered demo pensioners"
    )

    records = get_all_pensioners()

    if records:

        df = pd.DataFrame(records)

        df["account_number"] = df["account_number"].apply(
            lambda value: "XXXX" + str(value)[-4:]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No pensioner records found."
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "AI Life Certificate Assistance — Educational Demonstration"
)
