import React from 'react'
import { Card } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';

function Event(props) {
  return (
    <Card style={{ width: '23rem' }} className="text-center mx-auto">
      <Card.Img style={{ width:200, height:200  }} variant="top" src="/images/foodoor.png" className="mx-auto"/>
      <Card.Body style={{ width: '23rem' }}>
        <Card.Title>Number of orders</Card.Title>
        <Card.Text>
          {props.events.numEvent1}
        </Card.Text>
        <Card.Title>Number of payments</Card.Title>
        <Card.Text>
          {props.events.numEvent2}
        </Card.Text>
        <Card.Title>First order total</Card.Title>
        <Card.Text>
          {props.events.firstEvent1}
        </Card.Text>
        <Card.Title>First payment restaurant</Card.Title>
        <Card.Text>
          {props.events.firstEvent2}
        </Card.Text>
        <Card.Footer>
          <small className="text-muted">Last updated {props.events.updatedTimestamp}</small>
        </Card.Footer>
      </Card.Body>
    </Card>
  )
  // return (<div>{props.quote}</div>)
}

export default Event