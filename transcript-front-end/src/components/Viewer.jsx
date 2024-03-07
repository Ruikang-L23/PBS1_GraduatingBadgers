import { useContext } from "react";
import CurrentTranscriptContext from "../CurrentTranscriptContext";

export default function Viewer(props) {

    const [transcript, setTranscript] = useContext(CurrentTranscriptContext)

    return (
        <div>
            <h1>Transcript Viewer Page</h1>
            {
                transcript 
                ? <div dangerouslySetInnerHTML={{ __html: transcript }} />
                : <p>Please upload a caption file using the upload page.</p>
            }
        </div>
    );

}