import streamlit as st
import requests
import pandas as pd
import concurrent.futures


class SiteConnectivityChecker:
    """Manages site connectivity checking with Streamlit UI."""

    def __init__(self):
        # Use session state to persist URLs across reruns
        if "urls" not in st.session_state:
            st.session_state.urls = {}
        self.URLs = st.session_state.urls

    def check_site_connectivity(self, url: str) -> bool:
        """Check if a URL is accessible (returns True if status code is 200)."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }
            response = requests.get(url, timeout=5, headers=headers)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"{e}")
            return False

    def create_dashboard(self):
        """Create and render the Streamlit dashboard interface."""
        st.session_state.url_list = self.URLs

        st.title(":link: Site Connectivity Checker")
        new_url = st.text_input("Enter URL", value="https://www.google.com")

        # Add new URL to the list
        if (
            st.button("Add URL", use_container_width=True, type="secondary")
            and new_url not in self.URLs
        ):
            self.URLs[new_url] = False
            st.session_state.urls = self.URLs  # Persist to session state
            st.write(f"len is {len(self.URLs)}")

        data = {"URL": [self.URLs.keys], "Status": [self.URLs.values]}
        df = pd.DataFrame(data)

        # Display URL list with status and delete option
        st.write("URLs' status")
        for row in self.URLs:
            col1, col2, col3 = st.columns([2.5, 1, 1], border=True)
            with col1:
                st.write(row)
            with col2:
                if self.URLs.get(row):
                    st.write(self.URLs.get(row))
                else:
                    st.write(f":red[{self.URLs.get(row)}]")
            with col3:
                if st.button("", key=row, icon="❌"):
                    del self.URLs[row]
                    st.session_state.urls = (
                        self.URLs
                    )  # Persist deletion to session state
                    st.rerun()  # Refresh the page to reflect the deletion

        # Check connectivity for all URLs using thread pool
        if st.button("Check connectivity", type="primary"):
            for url in self.URLs:
                with st.spinner(f"Checking {url}"):
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(self.check_site_connectivity, url)
                        self.URLs[url] = future.result()
            st.session_state.urls = self.URLs  # Persist updated status


if __name__ == "__main__":
    site_connectivity_checker = SiteConnectivityChecker()
    site_connectivity_checker.create_dashboard()
