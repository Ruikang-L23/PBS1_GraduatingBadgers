import { Navbar, Container, Nav } from 'react-bootstrap';
import { Link, Outlet } from 'react-router-dom';

export default function Navigation() {

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
                <Outlet />
            </div>
        </div>
    );

}