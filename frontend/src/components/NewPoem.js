import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function NewPoem() {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    const handleSubmit = (event) => {
        event.preventDefault();
        fetchNewPoem(event.target.form[0].value, event.target.form[1].value, token);
    };

    const fetchNewPoem = (title, body, token) => {
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
            body: `{"title":"${title}","body":"${body}"}`,
        };

        console.log(options);

        fetch('http://127.0.0.1:8000/poems/new', options)
            .then((response) => response.json())
            .then((response) => console.log(response))
            .catch((err) => console.error(err));
    };

    return (
        <div>
            <form>
                <label htmlFor="title">Title</label>
                <input type="text" id="title" name="title" />
                <label htmlFor="body">Body</label>
                <input type="text" id="body" name="body" />
                <input type="submit" value="Submit new poem" onClick={handleSubmit} />
                <input type="submit" value="Back" onClick={() => navigate('/my-poems')} />
            </form>
        </div>
    );
}
