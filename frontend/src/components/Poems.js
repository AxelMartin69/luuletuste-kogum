import React from 'react';

export default function Poems(props) {
    return (
        <div key={props.id}>
            <h1>{props.title}</h1>
            <p>{props.body}</p>
            <ul>
                <li>{props.author}</li>
                <li>{props.entry_time}</li>
                <li>{props.likes}</li>
            </ul>
        </div>
    );
}
