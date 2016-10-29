import React, { Component } from 'react';

import FoodItem from './FoodItem.jsx';

// Add component - represents the whole app
export default class App extends Component {
    getItems() {
        return [
            { _id: 1, text: 'This is Item 1' },
            { _id: 2, text: 'This is Item 2' },
            { _id: 3, text: 'This is Item 3' },
        ];
    }

    renderItems() {
        return this.getItems().map((item) => (
            <FoodItem key={item._id} item={item} />
        ));
    }

    render() {
        return (
            <div className="container">
                <header>
                     <h1>Food List</h1>
                </header>
            <ul>
                { this.renderItems() }
            </ul>
            </div>
        );
     }
}
