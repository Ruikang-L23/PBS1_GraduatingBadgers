import { useState } from "react";
import { Button } from "react-bootstrap";
import { Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

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
            <Form>
                <Form.Group>
                    <Form.Label>Caption File</Form.Label>
                    <Form.Control type="file" onChange={handleFileUpload}></Form.Control>
                    <Form.Text className="text-muted">Accepts only SRT and SCC caption files.</Form.Text>
                </Form.Group>
                <Button onClick={handleSubmit}>
                    Submit
                </Button>
            </Form>
        </div>
    );

}