import { useState } from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import { Link, Outlet } from 'react-router-dom';
import CurrentTranscriptContext from '../CurrentTranscriptContext';

export default function Navigation() {

    const [transcript, setTranscript] = useState(0);

    return (
        <div>
            <Navbar bg="dark" variant="dark" sticky="top">
                <Container>
                    <Navbar.Brand as={Link} to="/">Transcript Translator</Navbar.Brand>
                    <Nav>
                        <Nav.Link as={Link} to="/">Home</Nav.Link>
                        <Nav.Link as={Link} to="/upload">Upload</Nav.Link>
                        <Nav.Link as={Link} to="/viewer">View</Nav.Link>
                    </Nav>
                </Container>
            </Navbar>
            <div style={ { margin: "1rem" } }>
                <CurrentTranscriptContext.Provider value={[transcript, setTranscript]}>
                    <Outlet />
                </CurrentTranscriptContext.Provider>
            </div>
        </div>
    );

}