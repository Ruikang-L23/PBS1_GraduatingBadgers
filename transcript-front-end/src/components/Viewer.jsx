import { useContext } from "react";
import CurrentTranscriptContext from "../CurrentTranscriptContext";

export default function Viewer(props) {

    const [transcript, setTranscript] = useContext(CurrentTranscriptContext)

    // We will need to update how the transcript is printed out once PBS-38 is finished.

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