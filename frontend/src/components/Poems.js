import React from 'react';

export default function Poems(props) {
    const token = localStorage.getItem('token');

    const handleLike = (token) => {
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
        };

        fetch(`http://127.0.0.1:8000/poems/like/${props.poem_id}`, options)
            .then((response) => response.json())
            .then((response) => console.log(response))
            .catch((err) => console.error(err));
    };
    return (
        <div key={props.id}>
            <h1>{props.title}</h1>
            <p>{props.body}</p>
            <ul>
                <li>Autor: {props.author}</li>
                <li>Loodud: {props.entry_time}</li>
                {props.token ? (
                    <li>
                        <button onClick={() => handleLike(token)}>Likes: {props.likes}</button>
                    </li>
                ) : (
                    <li>Likes: {props.likes}</li>
                )}
            </ul>
        </div>
    );
}
