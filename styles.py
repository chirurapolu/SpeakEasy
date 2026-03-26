custom_css = """
<style>
    :root {
        --primary: #4361ee;
        --secondary: #3f37c9;
        --accent: #4895ef;
        --light: #f8f9fa;
        --dark: #212529;
        --success: #4cc9f0;
        --warning: #f72585;
    }

    .main {
        background-color: #e0f2f7; /* Light blue background */
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    .stApp {
        background: transparent;
    }

    .header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        animation: fadeInDown 1s ease-out;
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0;
    }

    .nav-buttons {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
        gap: 15px;
    }

    .nav-button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px 30px;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 10px rgba(67, 97, 238, 0.3);
        animation: pulse 2s infinite alternate;
    }

    .nav-button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 15px rgba(67, 97, 238, 0.4);
    }

    .nav-button:active {
        transform: translateY(0);
        box-shadow: 0 2px 5px rgba(67, 97, 238, 0.3);
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        100% {
            transform: scale(1.05);
        }
    }

    .tab-content {
        background: transparent;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: none;
        min-height: 400px;
        animation: fadeInUp 1s ease-out;
        display: none; /* Initially hide the tab content */
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--dark);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .section-title:before {
        content: "";
        display: block;
        width: 5px;
        height: 25px;
        background: var(--primary);
        border-radius: 3px;
    }

    .stButton>button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 10px rgba(67, 97, 238, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px) scale(1.08);
        box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
        color: white;
    }

    .stButton>button:active {
        transform: translateY(0);
    }

    .stRadio>div {
        flex-direction: row !important;
        gap: 15px;
    }

    .stRadio [role="radiogroup"] {
        gap: 15px;
    }

    .stRadio [class*="st-"] {
        margin-bottom: 0;
    }

    .result-box {
        background: #f8fafc;
        border-left: 4px solid var(--primary);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        animation: fadeIn 1s ease-out;
    }

    /* Add this rule to make the text black */
    .result-box p {
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 0;
        color: var(--dark); /* Set the text color to dark */
    }

    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 3rem;
        color: #6c757d;
        font-size: 0.9rem;
        border-top: 1px solid rgba(0,0,0,0.1);
        animation: slideInUp 1s ease-out;
    }

    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Removed buggy custom widget CSS, relying on Streamlit native theme */

    /* Success message */
    .stAlert {
        border-radius: 8px !important;
        background-color: var(--success) !important;
        color: var(--light) !important;
        font-weight: bold;
    }

    /* Warning message */
    .stAlert.st-warning {
        background-color: var(--warning) !important;
        color: var(--light) !important;
        font-weight: bold;
    }

    /* Info message */
    .stAlert.st-info {
        background-color: var(--accent) !important;
        color: var(--light) !important;
        font-weight: bold;
    }

    /* Error message */
    .stAlert.st-error {
        background-color: #dc3545 !important;
        color: var(--light) !important;
        font-weight: bold;
    }

    /* Download button */
    .stDownloadButton>button {
        background-color: var(--success) !important;
        color: var(--light) !important;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: background-color 0.3s;
    }
    .stDownloadButton>button:hover {
        background-color: #20c997 !important;
    }

    /* Separate action buttons */
    .action-button-container {
        display: flex;
        gap: 10px;
        margin-top: 1rem;
    }
    .action-button {
        background: linear-gradient(90deg, var(--secondary) 0%, var(--primary) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(63, 55, 201, 0.3);
    }
    .action-button:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 5px 12px rgba(63, 55, 201, 0.4);
    }
    .action-button:active {
        transform: translateY(0);
    }
</style>
"""