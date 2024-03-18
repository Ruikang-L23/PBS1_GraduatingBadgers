import "./ViewerStyle.css";
import { useContext } from "react";
import CurrentTranscriptContext from "../CurrentTranscriptContext";
import aiIcon from "./icons/ai.svg"; 
import downloadIcon from "./icons/download.svg";
import noteIcon from "./icons/note.svg";
import fontIcon from "./icons/font.svg";

export default function Viewer(props) {

    const [transcript, setTranscript] = useContext(CurrentTranscriptContext)

    // We will need to update how the transcript is printed out once PBS-38 is finished.

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
            <h1>Transcript Viewer Page</h1>
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