import streamlit as st

# تنظیمات صفحه
st.set_page_config(page_title="Particles.js in Streamlit", layout="wide")

# افزودن پس‌زمینه با HTML و CSS
st.markdown("""
    <style>
        #particles-js {
            position: fixed;
            width: 100vw;
            height: 100vh;
            top: 0;
            left: 0;
            z-index: -1;
        }
        .stApp {
            background: transparent;
        }
    </style>

    <div id="particles-js"></div>

    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            particlesJS("particles-js", {
              "particles": {
                "number": {
                  "value": 100,
                  "density": {
                    "enable": true,
                    "value_area": 800
                  }
                },
                "color": {
                  "value": "#ffffff"
                },
                "shape": {
                  "type": "circle",
                  "stroke": {
                    "width": 0,
                    "color": "#000000"
                  }
                },
                "opacity": {
                  "value": 0.5,
                  "random": false
                },
                "size": {
                  "value": 2,
                  "random": true
                },
                "line_linked": {
                  "enable": true,
                  "distance": 100,
                  "color": "#ffffff",
                  "opacity": 0.22,
                  "width": 1
                },
                "move": {
                  "enable": true,
                  "speed": 0.2,
                  "direction": "none",
                  "random": false
                }
              },
              "interactivity": {
                "detect_on": "canvas",
                "events": {
                  "onhover": {
                    "enable": true,
                    "mode": "grab"
                  },
                  "onclick": {
                    "enable": true,
                    "mode": "repulse"
                  }
                }
              },
              "retina_detect": true
            });
        });
    </script>
""", unsafe_allow_html=True)

# **محتوای اصلی اپلیکیشن**
st.title("افکت Particles.js در پس‌زمینه استریم‌لیت")
st.write("پس‌زمینه پویا و جذاب اضافه شد!")
st.button("دکمه کلیک")
