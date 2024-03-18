import "./ViewerStyle.css";
import { useContext, useEffect } from "react";
import CurrentTranscriptContext from "../CurrentTranscriptContext";
import aiIcon from "./icons/ai.svg"; 
import downloadIcon from "./icons/download.svg";
import noteIcon from "./icons/note.svg";
import fontIcon from "./icons/font.svg";

export default function Viewer(props) {

    const [transcript, setTranscript] = useContext(CurrentTranscriptContext);

    function createTimestampBubble(startTime, endTime) {
        const bubble = document.createElement('div');
        bubble.classList.add('timestamp-bubble');
        bubble.textContent = `start: ${startTime}, end: ${endTime}`;
        return bubble;
    }
      
    function updateBubblePosition(event, bubble) {
        const offsetX = 10;
        const offsetY = -30; // Adjust the offset to position the bubble above the cursor
        bubble.style.left = event.pageX + offsetX + 'px';
        bubble.style.top = event.pageY + offsetY + 'px';
    }

    useEffect(() => {
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
    }, [transcript]);

    const handleDownload = () => {
        // Logic for downloading the transcript
    };

    const handleFontSize = () => {
        // Logic for adjusting the font size
    };

    const handleAI = () => {
        // Logic for AI interaction
    };

    const handleNotes = () => {
        // Logic for taking notes
    };

    return (
        <div>
            <h1>Transcript</h1>
            {
                transcript 
                ? <div dangerouslySetInnerHTML={{ __html: transcript }} />
                : <p>Please upload a caption file using the upload page.</p>
            }
            <div className="toolbar"> {/* Make sure the class name is a string */}
                <button className="iconButton" onClick={handleDownload}>
                    <img src={downloadIcon} alt="Download" /> {/* Use img tags for imported SVGs */}
                </button>
                <button className="iconButton" onClick={handleFontSize}>
                    <img src={fontIcon} alt="Font Size" />
                </button>
                <button className="iconButton" onClick={handleNotes}>
                    <img src={noteIcon} alt="Notes" />
                </button>
                <button className="iconButton" onClick={handleAI}>
                    <img src={aiIcon} alt="AI" />
                </button>
            </div>
        </div>
    );
}