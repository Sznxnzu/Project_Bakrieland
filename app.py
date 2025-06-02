col_header_left, col_header_right = st.columns([0.8, 0.2])
with col_header_right:
    col_00, col_01 = st.columns([0.5, 0.5])
    with col_00:
        st.markdown("""
        <div style='display: flex; align-items: flex-end; height: 100%; justify-content: flex-start;'>
            <p style='font-size: 0.8em; color:#aaa; margin: 0;'>POWERED BY</p>
        </div>
        """, unsafe_allow_html=True)

    with col_01:
        st.markdown("""
        <div style='text-align: right;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png' width='120' style='margin: 5px;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='50' style='margin: 5px;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='50' style='margin: 5px;'>
        </div>
        """, unsafe_allow_html=True)

    # Tambahkan robot 3D di bawah logo
    st.markdown("### 🤖 Robot Interaktif")
    components.html(
        """
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

        <model-viewer id="robot" 
            src="https://cdn.jsdelivr.net/gh/husnanali05/FP_Datmin@main/cute-robot-colored.glb"
            alt="Cute Robot Colored 3D"
            camera-controls 
            auto-rotate 
            autoplay
            style="width: 100%; height: 400px;"
            ar 
            shadow-intensity="1"
            environment-image="neutral"
            exposure="1"
            interaction-prompt="none">
        </model-viewer>

        <script>
          const robot = document.querySelector("#robot");
          robot.addEventListener("click", () => {
            robot.currentTime = 0;
            robot.play();
          });
        </script>
        """,
        height=420
    )
