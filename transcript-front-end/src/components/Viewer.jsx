import "./ViewerStyle.css";
import { useContext, useEffect, useState } from "react";
import CurrentTranscriptContext from "../CurrentTranscriptContext";
import aiIcon from "./icons/ai.svg"; 
import downloadIcon from "./icons/download.svg";
import contrastModeIcon from "./icons/contrastMode.svg";
import increaseFontSizeIcon from './icons/increaseFontSize.svg'
import decreaseFontSizeIcon from './icons/decreaseFontSize.svg'

export default function Viewer(props) {

    const [transcript, setTranscript] = useContext(CurrentTranscriptContext);
    const [darkMode, setDarkMode] = useState(false);
    const [aiFormatActive, setAIFormatActive] = useState(false);
    const [fontSize, setFontSize] = useState(0);
    const [transcriptHeaderText, setTranscriptHeaderText] = useState('Transcript');

    function createTimestampBubble(startTime, endTime) {
        const bubble = document.createElement('div');
        bubble.classList.add('timestamp-bubble');
        bubble.textContent = `start: ${startTime}, end: ${endTime}`;
        return bubble;
    }
      
    function updateBubblePosition(event, bubble) {
        const offsetX = 10;
        const offsetY = -30; // Adjust the offset to position the bubble above the cursor.
        bubble.style.left = event.pageX + offsetX + 'px';
        bubble.style.top = event.pageY + offsetY + 'px';
    }

    /* A state change to either transcript or aiFormatActive will cause this function to be run.
       The function changes the header text based on the current state of aiFormatActive.
       If timestamps are enabled on a given transcript, it also creates event listeners for each <p> tag.
    */
    useEffect(() => {
        if (!aiFormatActive) {
            setTranscriptHeaderText('Transcript');
        } else {
            setTranscriptHeaderText('Transcript (AI-modified)');
        }
        if (transcript && transcript.options.enableTimestamps) {
            const paragraphs = document.querySelectorAll('p');
            paragraphs.forEach(paragraph => {
                paragraph.addEventListener('mouseover', event => {
                    paragraph.classList.add('highlight');
                    const startTime = paragraph.getAttribute('data-timestamp-start');
                    const endTime = paragraph.getAttribute('data-timestamp-end');
                    const bubble = createTimestampBubble(startTime, endTime);
                    document.body.appendChild(bubble);
            
                    // Position the bubble next to the cursor
                    updateBubblePosition(event, bubble);
                    
                    // Update the bubble position as the cursor moves
                    document.addEventListener('mousemove', event => {
                        updateBubblePosition(event, bubble);
                    });
                });
                paragraph.addEventListener('mouseout', () => {
                    paragraph.classList.remove('highlight');
                    const bubble = document.querySelector('.timestamp-bubble');
                    if (bubble) {
                        bubble.remove();
                    }
                });
            });
        }
    }, [transcript, aiFormatActive]);

    /* A state change to either fontSize or darkMode will cause this function to be run.
       The function simply finds all of the <p> tags and the header, updating their styling. 
    */
    useEffect(() => {
        const paragraphs = document.querySelectorAll('p');
        const header = document.getElementById('transcriptHeader');
        if (darkMode) {
            document.body.style = 'background: black;';
            paragraphs.forEach(paragraph => paragraph.classList.add('dark-mode'));
            header.classList.add('dark-mode');
        } else {
            document.body.style = 'background: white;';
            paragraphs.forEach(paragraph => paragraph.classList.remove('dark-mode'));
            header.classList.remove('dark-mode');
        }
        paragraphs.forEach(paragraph => paragraph.style.setProperty('font-size', (1 + (fontSize * 0.15) + "rem")));
        header.style.setProperty('font-size', (2 + (fontSize * 0.3) + "rem"));
    }, [fontSize, darkMode]);

    const handleDownload = () => {
        const transcriptToDL = transcript.options.enableAI ? transcript.transcripts.aiTranscript : transcript.transcripts.baseTranscript;
        const blob = new Blob([transcriptToDL], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'transcript.html'; // Name of the file to be downloaded
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div>
            <h1 id="transcriptHeader">{transcriptHeaderText}</h1>
            {
                transcript 
                ? !aiFormatActive 
                  ? <div dangerouslySetInnerHTML={{ __html: transcript.transcripts.baseTranscript }} />
                  : transcript.transcripts.aiTranscript 
                    ? <div dangerouslySetInnerHTML={{ __html: transcript.transcripts.aiTranscript }} />
                    : <p>Artificial intelligence transcription has not yet completed.</p>
                : <p>Please upload a caption file using the upload page.</p>
            }
            {
                transcript
                ? <div className="toolbar">
                    <button className="iconButton" title="Download File" onClick={handleDownload}>
                        <img src={downloadIcon} alt="Download" />
                    </button>
                    <button className="iconButton" title="Increase Font Size" disabled={fontSize >= 2} onClick={() => setFontSize((count) => count + 1)}>
                        <img src={increaseFontSizeIcon} alt="Increase Font Size" />
                    </button>
                    <button className="iconButton" title="Decrease Font Size" disabled={fontSize <= -2} onClick={() => setFontSize((count) => count - 1)}>
                        <img src={decreaseFontSizeIcon} alt="Decrease Font Size" />
                    </button>
                    <button className="iconButton" title={darkMode ? "Light Mode" : "Dark Mode"} onClick={() => setDarkMode((old) => !old)}>
                        <img src={contrastModeIcon} alt={darkMode ? "Light Mode" : "Dark Mode"} />
                    </button>
                    { 
                        transcript.options.enableAI && 
                        <button className="iconButton" title={aiFormatActive ? "View Standard Transcription" : "View AI Transcription"} onClick={() => setAIFormatActive((old) => !old)}>
                            <img src={aiIcon} alt={aiFormatActive ? "View Standard Transcription" : "View AI Transcription"} />
                        </button>
                    }
                  </div>
                : <></>
            }
        </div>
    );
}
