import { useState } from "react";
import { Button } from "react-bootstrap";
import { Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import '../App.css';

export default function UploadPage(props) {

    const [file, setFile] = useState(0);
    let navigator = useNavigate();

    const handleFileUpload = (e) => {
        e.preventDefault();
        // May need to add a check here to make sure the file is an SCC or SRT file but this could also be done in the backend.
        const files = e.target.files;
        setFile(files[0]);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        // This is where our API call would go.
        console.log(file);
        navigator("/viewer");
    }

    // Additional options for formatting could be added to this Form later (e.g somebody choosing whether to italize sounds).

    return (
        <div>
            <h1>Upload Page</h1>
            <div className="center-card">
                <Form>
                    <Form.Group>
                        <Form.Label style={ { marginBottom: "1.5rem" } }>Caption File</Form.Label>
                        <Form.Control type="file" className="caption-upload" onChange={handleFileUpload}></Form.Control>
                        <Form.Text className="text-muted">Accepts only SRT and SCC caption files.</Form.Text>
                    </Form.Group>
                    <Button onClick={handleSubmit} variant="outline-dark" disabled={file == 0} style={ { marginTop: "1.5rem" } }>
                        Submit
                    </Button>
                </Form>
            </div>
        </div>
    );

}