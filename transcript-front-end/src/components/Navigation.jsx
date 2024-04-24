import { useState } from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import { Link, Outlet } from 'react-router-dom';
import CurrentTranscriptContext from '../CurrentTranscriptContext';
import logo from './images/logo.png'

export default function Navigation() {

    const [transcript, setTranscript] = useState(false);

    return (
        <div>
            <Navbar bg="dark" variant="dark" sticky="top">
                <Container>
                    <Navbar.Brand as={Link} to="/">
                        <img
                            src={logo}
                            alt="PBS Wisconsin"
                            width="25%" 
                            height="auto" 
                            className="d-inline-block align-top"
                        />
                    </Navbar.Brand>
                    <Nav>
                        <Nav.Link as={Link} to="/">Home</Nav.Link>
                        <Nav.Link as={Link} to="/upload">Upload</Nav.Link>
                        <Nav.Link as={Link} to="/viewer">View</Nav.Link>
                    </Nav>
                </Container>
            </Navbar>
            <div style={{ margin: "0" }}>
                <CurrentTranscriptContext.Provider value={[transcript, setTranscript]}>
                    <Outlet />
                </CurrentTranscriptContext.Provider>
            </div>
        </div>
    );

}