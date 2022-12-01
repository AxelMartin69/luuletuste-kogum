import React from 'react';

export default function Poems(props) {
    const handleLike = () => {
        console.log(`liked: ${props.title}, ${props.id}`);
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
                        <button onClick={handleLike}>Likes: {props.likes}</button>
                    </li>
                ) : (
                    <li>Likes: {props.likes}</li>
                )}
            </ul>
        </div>
    );
}
