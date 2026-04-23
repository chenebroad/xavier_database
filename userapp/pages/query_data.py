import streamlit as st
import pandas as pd
from api_client import query_data, run_quick_query, update_row

st.title("🔍 Query Data")

edit_data = st.toggle("Edit data")

tab1, tab2 = st.tabs(["Whole Display", "Quick Queries"])

with tab1:
    st.subheader("To see all available data")
    # -------------------------
    # TABLE SELECTION
    # -------------------------
    tables = [
        "projects",
        "samples",
        "experiments",
        "sequencing_runs",
        "run_experiments",
        "seqexp",
        "files"
    ]

    selected_table = st.selectbox("Select Table", tables)

    limit = st.number_input("Row Limit", min_value=1, max_value=10000, value=100)

    # -------------------------
    # RUN QUERY
    # -------------------------
    if st.button("Run Query"):
        try:
            data = query_data(selected_table, limit)

            if not data:
                st.warning("No data found.")
                st.session_state.df = None
                st.session_state.edited_df = None
                st.session_state.original_df = None
            else:
                df = pd.DataFrame(data)

                st.session_state.df = df
                st.session_state.edited_df = df.copy()
                st.session_state.original_df = df.copy()

        except Exception as e:
            st.error("Query failed")
            st.write(type(e))
            st.write(e)


    # -------------------------
    # SAFE NORMALIZER
    # -------------------------
    def normalize(row: dict):
        return {
            k: (None if v == "" else v)
            for k, v in row.items()
        }


    # -------------------------
    # DISPLAY SECTION
    # -------------------------
    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Current Data",
            csv,
            f"{selected_table}.csv",
            "text/csv"
        )

        # -------------------------
        # EDIT MODE
        # -------------------------
        if edit_data:
            st.subheader("✏️ Edit Data")

            edited_df = st.data_editor(
                st.session_state.edited_df,
                width="stretch",
                num_rows="fixed",
                key="data_editor"
            )

            # ONLY update session state if changed
            if not edited_df.equals(st.session_state.edited_df):
                st.session_state.edited_df = edited_df
            
            st.subheader("Upload Edited Data")

            uploaded_file = st.file_uploader("Upload edited CSV", type=["csv"])

            if uploaded_file:
                try:
                    edited_df = pd.read_csv(uploaded_file)

                    st.write("Preview of uploaded data:")
                    st.dataframe(edited_df, width="content")
                
                except Exception as e:
                    st.error(f"Failed to read file: {e}")

            # -------------------------
            # SAVE CHANGES
            # -------------------------
            if st.button("Apply Uploaded Changes"):

                original_df = st.session_state.df

                changes_made = False
                errors = []

                for i in range(len(edited_df)):

                    original = original_df.iloc[i].to_dict()
                    edited = edited_df.iloc[i].to_dict()

                    def normalize(row):
                        return {k: (None if v == "" else v) for k, v in row.items()}

                    if normalize(original) != normalize(edited):
                        changes_made = True

                        row_id = original.get("id")

                        payload = {
                            k: (None if v == "" else v)
                            for k, v in edited.items()
                            if k not in ["id", "created_at", "updated_at"]
                        }

                        try:
                            update_row(selected_table, row_id, payload)
                        except Exception as e:
                            errors.append({"row": i, "error": str(e)})

                if errors:
                    st.error("Some rows failed:")
                    st.write(errors)

                elif changes_made:
                    st.success("Changes applied successfully")

                    # refresh
                    data = query_data(selected_table, limit)
                    st.session_state.df = pd.DataFrame(data)

                else:
                    st.info("No changes detected")


        # -------------------------
        # VIEW MODE
        # -------------------------
        else:
            st.subheader("📄 View Data")

            st.success(f"Returned {len(df)} rows")

            st.dataframe(df, use_container_width=True)

    # # -------------------------
    # # QUERY BUTTON
    # # -------------------------
    # if st.button("Run Query"):
    #     try:
    #         data = query_data(selected_table, limit)

    #         if not data:
    #             st.warning("No data found.")
    #             st.session_state.df = None
    #         else:
    #             df = pd.DataFrame(data)

    #             # Store BOTH original + editable copy
    #             st.session_state.df = df
    #             st.session_state.edited_df = df.copy()

    #     except Exception as e:
    #         st.error("Query failed")
    #         st.write(type(e))
    #         st.write(e)
            
    # if "df" in st.session_state and st.session_state.df is not None:

    #     df = st.session_state.df

    #     if edit_data:
    #         st.subheader("✏️ Edit Data")

    #         edited_df = st.data_editor(
    #             st.session_state.edited_df,
    #             width="stretch",
    #             num_rows="fixed",
    #             key="data_editor"
    #         )

    #         # Persist edits across reruns
    #         if not edited_df.equals(st.session_state.edited_df):
    #             st.session_state.edited_df = edited_df

    #         # -------------------------
    #         # SAVE CHANGES
    #         # -------------------------
    #         if st.button("Save Changes"):
    #             changes_made = False

    #             for i in range(len(df)):
    #                 original = df.iloc[i].to_dict()
    #                 edited = edited_df.iloc[i].to_dict()

    #                 if original != edited:
    #                     changes_made = True

    #                     row_id = original.get("id")

    #                     # Remove immutable fields
    #                     payload = {
    #                         k: (None if v == "" else v)
    #                         for k, v in edited.items()
    #                         if k not in ["id", "created_at", "updated_at"]
    #                     }

    #                     try:
    #                         update_row(selected_table, row_id, payload)
    #                     except Exception as e:
    #                         #st.error(f"Row {i} failed: {e}")
    #                         pass

    #             if changes_made:
    #                 st.success("Changes saved successfully")

    #                 # Refresh data after save
    #                 data = query_data(selected_table, limit)
    #                 new_df = pd.DataFrame(data)

    #                 st.session_state.df = new_df
    #                 st.session_state.edited_df = new_df.copy()

    #             else:
    #                 st.info("No changes detected")

    #     else:
    #         st.subheader("📄 View Data")

    #         st.success(f"Returned {len(df)} rows")

    #         st.dataframe(df, width="stretch")

    #         csv = df.to_csv(index=False).encode("utf-8")
    #         st.download_button(
    #             "Download CSV",
    #             csv,
    #             f"{selected_table}.csv",
    #             "text/csv"
    #         )

with tab2:
    st.title("⚡ Quick Queries")

    query_type = st.selectbox(
        "Select Query",
        [
            "All Samples from Project",
            "All Experiments from Sample",
            "All Files from Sample",
            "All Files from Project"
        ]
    )

    if query_type == "All Samples from Project":
        project_name = st.text_input("Project Name")

    elif query_type == "All Experiments from Sample":
        sample_name = st.text_input("Sample Name")

    elif query_type == "All Files from Sample":
        sample_name = st.text_input("Sample Name")

    elif query_type == "All Files from Project":
        project_name = st.text_input("Project Name")
    
    if st.button("Run Quick Query"):
        try:
            if query_type == "All Files from Project":
                data = run_quick_query(
                    "files_by_project",
                    project_name=project_name
    )
            elif query_type == "All Experiments from Sample":
                data = run_quick_query(
                    "experiments_by_sample",
                    sample_name=sample_name)

            elif query_type == "All Files from Sample":
                data = run_quick_query(
                    "files_by_sample",
                    sample_name=sample_name)

            elif query_type == "All Samples from Project":
                data = run_quick_query(
                    "samples_by_project",
                    project_name=project_name)

            df = pd.DataFrame(data)

            if df.empty:
                st.warning("No results found")
            else:
                st.success(f"{len(df)} rows returned")
                st.dataframe(df, width="stretch")

        except Exception as e:
            st.error("Query failed")
            st.write(e)