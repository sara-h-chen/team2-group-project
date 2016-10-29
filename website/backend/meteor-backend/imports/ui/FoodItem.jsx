import React, { Component, PropTypes } from 'react';

// Food component - represents a single food item
export default class FoodItem extends Component {
    render() {
        return (
            <li>{ this.props.item.text }</li>
        );
    }
}

FoodItem.propTypes = {
    // This component gets the food item to display through a React prop.
    // We can use propTypes to indicate it is required
    item: PropTypes.object.isRequired,
};
