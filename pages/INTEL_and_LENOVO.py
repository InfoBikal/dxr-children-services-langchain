# pages/1_Intel_and_Lenovo.py
import streamlit as st

def show_intel_lenovo_page():
    """
    Displays the page detailing the TASP Chatbot, Intel technology integration,
    and the Intel + Lenovo partnership, adhering to Intel trademark guidelines.
    """
    st.set_page_config(
        page_title="Our Technology - DialogXR TASP Chatbot",
        page_icon="dialogXR_Icon.png",
        layout="wide"
    )

    st.title("🤖 DialogXR TASP Chatbot: Technology & Partnership")

    st.markdown(
        """
        Welcome to a deeper look into the technology that powers the
        DialogXR TASP Chatbot. This solution is designed to revolutionize how
        safeguarding professionals access critical information, supported by
        leading-edge AI and a strong technology partnership.
        """
    )

    st.header("Our Solution: AI-Powered Access to Safeguarding Knowledge")

    st.markdown(
        """
        The DialogXR TASP Chatbot, developed by BIKAL Tech UK Ltd for
        The Association of Safeguarding Partners (TASP), is integrated into
        TASP's ecosystem to provide seamless access to the National Society for
        the Prevention of Cruelty to Children (NSPCC) database. This repository
        contains approximately 1,400 Serious Case Reviews (SCRs).

        Our chatbot enables users to:
        - Obtain accurate answers to their queries regarding child safeguarding.
        - Directly download relevant SCR documents through an intuitive interface.
        """
    )

    st.subheader("Addressing a Critical Market Need")

    st.markdown(
        """
        Professionals and stakeholders in child safeguarding often require timely
        and precise information from SCRs to inform their practices and decisions.
        However, navigating extensive databases to find specific case information
        can be time-consuming and challenging.

        **Our chatbot aims to streamline access to this critical information,
        enhancing efficiency and effectiveness in safeguarding efforts.**
        """
    )

    st.header("Our Data-Driven Approach")

    st.markdown(
        """
        To provide accurate and relevant information, our system processes and
        analyzes data meticulously:
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Data Collection")
        st.markdown(
            """
            -   **Serious Case Reviews (SCRs):** Comprehensive reports from the
                NSPCC repository detailing cases of child abuse and neglect.
            -   **User Queries:** Questions inputted by users seeking information.
            -   **Usage Metrics:** Anonymized data on chatbot interaction patterns
                to help us improve the service.
            """
        )

    with col2:
        st.subheader("Data Analysis Process")
        st.markdown(
            """
            -   **Semantic Chunking of PDFs:** SCR documents (primarily PDFs) are
                divided into semantically meaningful sections.
            -   **Indexing in a Vector Database:** These chunks are converted into
                vector embeddings and indexed for efficient similarity searches.
            -   **Query Processing and Retrieval:** User queries are vectorized
                and matched against the database to retrieve the most relevant
                document chunks, ensuring precise responses.
            """
        )

    st.header("Enhanced by Intel® Technologies")

    st.image(
        "intel.png",
        width=150
        # caption="Intel® Logo"
    )


    st.markdown(
        """
        To ensure optimal performance, accuracy, and scalability, our chatbot
        leverages the power of Intel® technologies:
        """
    )


    st.subheader("1. Intel® oneAPI AI Analytics Toolkit")

    st.markdown(
        """
        This comprehensive toolkit offers optimized libraries and frameworks for
        end-to-end data science and machine learning pipelines.
        -   **Benefit:** It accelerates data preprocessing, model training, and
            inference tasks, ensuring efficient handling of user queries and
            rapid response generation from our RAG model.
        """
    )

    st.subheader("2. Intel® Extension for Transformers")

    st.markdown(
        """
        An innovative toolkit specifically designed to accelerate transformer-based
        models, which are foundational for modern Natural Language Processing (NLP)
        applications like our chatbot.
        -   **Benefit:** Integrating this extension significantly enhances the
            chatbot's ability to understand and process complex user queries
            effectively and efficiently.
        """
    )

    st.subheader("3. Intel® Distribution of OpenVINO™ toolkit")

    st.markdown(
        """
        The Intel® Distribution of OpenVINO™ toolkit (Open Visual Inference & Neural
        Network Optimization) facilitates the deployment of optimized deep learning
        models across various Intel® hardware platforms.
        -   **Benefit:** This ensures that the chatbot operates efficiently,
            delivering fast inference on Intel® CPUs and other Intel® hardware,
            and can scale effectively with increasing user demand and data volume.
        """
    )

    st.header("The Intel + Lenovo Advantage: Powering Reliable AI")

    st.image(
        "intel_lenovo_cropped.png",
        width=250,
        caption="AI Powered by Intel® and Lenovo"
    )

    st.markdown(
        """
        The sophisticated AI capabilities of our chatbot, amplified by Intel®
        software, run on robust and high-performance infrastructure. This 
        includes powerful hardware such as **Third-generation Intel® Xeon® Scalable
        processors**, where partners like **Lenovo** play a crucial role.
        Lenovo's enterprise-grade servers and workstations are renowned for:

        -   **Optimized Performance:** Lenovo systems are often co-engineered and
            validated to maximize the potential of Intel® processors (like the
            Intel® Xeon® Scalable processors) and AI software, ensuring our
            demanding AI workloads run smoothly.
        -   **Reliability and Scalability:** The dependability of Lenovo hardware
            is essential for the continuous, 24/7 operation of our chatbot services.
            It also provides a scalable foundation to grow as our user base and
            data requirements expand.
        -   **Innovation Focus:** The collaboration between Intel and Lenovo drives
            technological advancements, providing a cutting-edge platform for
            AI solutions like ours.

        This powerful synergy between Intel's advanced software and high-performance
        hardware (exemplified by Lenovo's offerings featuring Intel® architecture)
        ensures that the DialogXR TASP Chatbot is built on a foundation of speed,
        efficiency, and trustworthiness.
        """
    )

    st.subheader("Delivering Business Value to End Users")
    st.markdown(
        """
        Ultimately, this technological foundation translates to tangible benefits
        for safeguarding professionals:
        -   **Efficiency:** Significantly reduces the time and effort required to
            locate specific SCR information.
        -   **Accessibility:** Provides a user-friendly interface for navigating
            complex and extensive databases.
        -   **Informed Decision-Making:** Empowers professionals to make quicker,
            better-informed decisions by providing rapid access to relevant case
            studies, findings, and recommendations.
        """
    )

    st.markdown("---")

    st.caption(
        """
        The DialogXR TASP Chatbot is a testament to how advanced AI,
        powered by Intel® technologies and supported by robust infrastructure partners
        like Lenovo, can deliver impactful solutions.
        Designed by BIKAL Tech UK Ltd.
        """
    )


    st.markdown("---")
    st.markdown("<h6>Trademark Attributions:</h6>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.8em;'>"
        "Intel and the Intel logo are trademarks of Intel Corporation or its subsidiaries.<br>"
        "Intel, the Intel logo, and Xeon are trademarks of Intel Corporation or its subsidiaries.<br>"
        "Intel, the Intel logo, OpenVINO, and the OpenVINO logo are trademarks of Intel Corporation or its subsidiaries."
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    show_intel_lenovo_page()