import { useContext, useState, useCallback } from "react";
import { Button, Form, Spinner } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
// import { useDropzone } from "react-dropzone";
import CurrentTranscriptContext from "../CurrentTranscriptContext";
import '../App.css';

export default function UploadPage(props) {

    const [file, setFile] = useState(0);
    const [fileFormatTextClass, setFileFormatTextClass] = useState("text-muted");
    const [fileName, setFileName] = useState('');
    const [isUploading, setIsUploading] = useState(false);
    const [italicSwitchState, setItalicSwitchState] = useState(false);
    const [aiSwitchState, setAISwitchState] = useState(true);
    const [timestampState, setTimestampState] = useState(false);
    const [transcriptionMode, setTranscriptionMode] = useState('verbatim');
    const [transcript, setTranscript] = useContext(CurrentTranscriptContext);
    const validFileFormats = ['srt', 'scc'];
    let navigator = useNavigate();

    const handleFileUpload = (e) => {
        e.preventDefault();
        processFile(e.target.files[0]);
    }
    
    const handleDrop = useCallback(acceptedFiles => {
        processFile(acceptedFiles[0]);
    }, []);

    const processFile = (file) => {
        const fileName = file.name;
        if (validFileFormats.includes(fileName.split(".")[1])) {
            setFileFormatTextClass("text-muted");
            setFile(file);
            setFileName(fileName);
        } else {
            setFileFormatTextClass("text-danger");
            setFile(0);
            setFileName('');
        }
    };

    const {getRootProps, getInputProps, isDragActive} = useDropzone({ 
        handleDrop
    });

    const handleSubmit = (e) => {
        sessionStorage.clear()
        setTranscript(false)

        e.preventDefault();

        const formData = new FormData();
        formData.append('file', file);
        formData.append('italicizeCues', italicSwitchState);
        formData.append('enableTimestamps', timestampState);

        setIsUploading(true);

        fetch('http://localhost:5000/api/upload', {
            method: "POST",
            body: formData
        })
        .then(resp => {
            if (!resp.ok) {
                return resp.json().then(err => {
                    throw new Error(err.msg);
                });
            }
            return resp.text();
        })
        .then(text => {
            const transcriptData = {
                "options": {
                    "enableTimestamps": timestampState,
                    "enableAI": aiSwitchState
                },
                "transcripts": {
                    "baseTranscript": text,
                    "aiTranscript": false
                }
            } 
            setTranscript(transcriptData);
            sessionStorage.setItem('transcriptData', JSON.stringify(transcriptData));
            navigator("/viewer");
            setIsUploading(false);

            if (aiSwitchState) {
                formData.append('transcriptionMode', transcriptionMode);

                fetch('http://localhost:5000/api/upload-ai', {
                    method: "POST",
                    body: formData
                })
                .then(resp => {
                    if (!resp.ok) {
                        return resp.json().then(err => {
                            throw new Error(err.msg);
                        });
                    }
                    return resp.text();
                })
                .then(text => {
                    transcriptData.transcripts.aiTranscript = text;
                    setTranscript(transcriptData);
                    sessionStorage.setItem('transcriptData', JSON.stringify(transcriptData));
                    console.log(text);
                })
            } 
        })
        .catch(error => {
            console.log(error);
            setIsUploading(false);
        })
    }

    return (
        <div style={ { margin: "1rem" } }> 
            <h1>Upload</h1>
            <div className="center-card">
                <Form>
                    <Form.Group>
                        <Form.Label style={ { marginBottom: "1.5rem" } }>Caption File</Form.Label>
                        <div {...getRootProps()} className="dropzone">
                            <input {...getInputProps()} />
                            {fileName ? (
                                <p className="text-success">Uploaded: {fileName}</p>
                            ) : (
                                <p>{isDragActive ? "Drop the files here ..." : "Drag 'n' drop some files here, or click to select files below"}</p>
                            )}
                            <Form.Control type="file" className="caption-upload" onChange={handleFileUpload}></Form.Control>
                        </div>
                        <Form.Text className={fileFormatTextClass}>Accepts only SRT and SCC caption files.</Form.Text>
                    </Form.Group>
                    <Form.Group>
                        <Form.Label style={ { marginTop: "1.5rem" } }>Transcription Options</Form.Label>
                        <div className="labeled-switch">
                            <Form.Check
                                inline
                                name="verbatim-choice"
                                type='radio'
                                value='verbatim'
                                checked={transcriptionMode == 'verbatim'}
                                onChange={() => setTranscriptionMode('verbatim')}
                            />
                            <p className="radio-label">Verbatim</p>
                            <Form.Check
                                inline
                                disabled={!aiSwitchState}
                                name="verbatim-choice"
                                type='radio'
                                value='non-verbatim'
                                checked={transcriptionMode == 'non-verbatim'}
                                onChange={() => setTranscriptionMode('non-verbatim')}
                            />
                            <p className={aiSwitchState ? "radio-label" : "muted-radio-label"}>Non-Verbatim</p>
                        </div>
                        <div className="labeled-switch">
                            <Form.Check 
                                defaultChecked={aiSwitchState} 
                                onChange={() => {setAISwitchState((old) => !old); setTranscriptionMode('verbatim')}} 
                                type="switch"
                            />
                            <p className="option-label">Enable AI usage?</p>
                        </div>
                        <div className="labeled-switch">
                            <Form.Check 
                                defaultChecked={italicSwitchState} 
                                onChange={() => setItalicSwitchState((old) => !old)} 
                                type="switch"
                            />
                            <p className="option-label">Italicize non-verbal cues?</p>
                        </div>
                        <div className="labeled-switch">
                            <Form.Check 
                                defaultChecked={timestampState} 
                                onChange={() => setTimestampState((old) => !old)}
                                type="switch"
                            />
                            <p className="option-label">Include timestamps?</p>
                        </div>
                    </Form.Group>
                    { 
                        !isUploading 
                        ? <Button onClick={handleSubmit} variant="outline-dark" disabled={file == 0} style={ { marginTop: "1.5rem" } }>
                            Submit
                          </Button>
                        : <Spinner animation="border" role="status" style={ { marginTop: "1.5rem" } }/>
                    }
                </Form>
            </div>
        </div>
    );

}
