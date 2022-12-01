import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function LogIn() {
    const navigate = useNavigate();

    const fetchToken = (username, password) => {
        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ grant_type: 'password', username: username, password: password }),
        };

        fetch('http://127.0.0.1:8000/token', options)
            .then((response) => response.json())
            .then((response) => localStorage.setItem('token', response.access_token))
            .catch((err) => console.error(err));
    };

    const handleSubmit = (event) => {
        const username = event.target.form[0].value;
        const password = event.target.form[1].value;
        fetchToken(username, password);
        navigate('/');
    };

    return (
        <form>
            Username:
            <input type="text" name="name" placeholder="username" />
            Password:
            <input type="password" name="name" placeholder="password" />
            <input type="submit" value="Log In" onClick={handleSubmit} />
            <input type="submit" value="Cancel" onClick={navigate('/')} />
        </form>
    );
}
