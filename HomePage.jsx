import "./HomePage.css"
import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../components/images/logo.png'


export default function HomePage(props) {

    return (
        <div className="mainbody">
            <div className="div1">
                <div className="overlay div1a">
                    <h1 className="primary-font" style={{fontSize: '350%'}}>Transform Your <br></br>Subtitles Into<br></br>Web Ready Formats</h1>
                    <p className="secondary-font" style={{fontSize: '150%', padding: '20px'}}>Fast and easy, just a click away.</p>
                    <Link to="/upload">
                        <button className="secondary-font rounded-blur-button" style={{fontSize: '125%'}}>Convert now!</button>
                    </Link>
                </div>
            </div>
            <div className="text-image-section">
                <div className="text-content">
                    <h1 className="primary-font">Effortlessly convert SRT and SCC files into clean, accessible HTML with our state-of-the-art tools.</h1>
                </div>
                <div className="image-content">
                </div>
            </div>
            <div className="div2">
                <div className="overlay div1a">
                    <h1 className="primary-font" style={{padding: '20px'}}>Why Choose Our Services?</h1>
                    <h2 className="secondary-font" style={{fontSize: '150%', padding: '10px'}}>Accuracy and Reliability</h2>
                    <p className="secondary-font" style={{fontSize: '100%'}}>Experience the most accurate conversion, preserving all timing and text formatting.</p>
                    <br></br>
                    <h2 className="secondary-font" style={{fontSize: '150%', padding: '10px'}}>Speed and Efficiency</h2>
                    <p className="secondary-font" style={{fontSize: '100%'}}>Convert files in seconds, no matter how large, with our optimized processing power.</p>
                    <br></br>
                    <h2 className="secondary-font" style={{fontSize: '150%', padding: '10px'}}>User-Friendly Interface</h2>
                    <p className="secondary-font" style={{fontSize: '100%'}}>No technical expertise needed with our simple, intuitive interface.</p>
                </div>
            </div>
            <div className="process-section">
                <h2 className="primary-font" style={{fontSize: '250%', padding: '20px'}}>How it works</h2>
                <div className="process-steps">
                    <div className="step">
                        <div className="step-number">1</div>
                        <div className="step-details">
                            <h3 className="secondary-font">Upload</h3>
                            <p className="secondary-font">Start by uploading your .scc or .srt subtitle file</p>
                        </div>
                    </div>
                    <div className="step">
                        <div className="step-number">2</div>
                        <div className="step-details">
                            <h3 className="secondary-font">Convert</h3>
                            <p className="secondary-font">Our tool will automatically convert the file to clean, accessible HTML</p>
                        </div>
                    </div>
                    <div className="step">
                        <div className="step-number">3</div>
                        <div className="step-details">
                            <h3 className="secondary-font">View & Download</h3>
                            <p className="secondary-font">Once converted, you can view or download the HTML file</p>
                        </div>
                    </div>
                </div>
            </div>
            <div className="feature-section">
                <div className="feature">
                    <h3 className="primary-font">Free to use</h3>
                    <p className="secondary-font">Convert as many files as you need at no cost.</p>
                </div>
                <div className="feature">
                    <h3 className="primary-font">No limits</h3>
                    <p className="secondary-font">There are no limits on file size or conversion volume.</p>
                </div>
                <div className="feature">
                    <h3 className="primary-font">Lifetime access</h3>
                    <p className="secondary-font">Your converted HTML files are yours to keep forever.</p>
                </div>
            </div>
            <footer className="footer">
                <div className="footer-content">
                    <img src={logo} alt="PBS Wisconsin Logo" className="footer-logo" />
                    <span className="footer-rights">Copyright © 2024 All rights reserved.</span>
                </div>
            </footer>
        </div>
    );
}