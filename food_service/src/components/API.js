import React, {useState, useEffect} from 'react'
import Event from "./event";
import axios from 'axios'

function API() {
  const [event, setData] = useState("")


  const getData = () => {
    Promise.all([
      axios.get("http://kafka-lab.westus2.cloudapp.azure.com:8100/orders/get_stats"),
      axios.get("http://kafka-lab.westus2.cloudapp.azure.com:8110/add_foods?index=0"),
      axios.get("http://kafka-lab.westus2.cloudapp.azure.com:8110/payments?index=0")
    ]).then(arr => {
      console.log("arr", arr);
      setData({
        numEvent1: arr[0].data["num_order"],
        numEvent2: arr[0].data["num_payment"],
        // Assuming there is a timestamp in your stats
        updatedTimestamp: arr[0].data["timestamp"],
        firstEvent1: arr[1].data["order_total"],  
        firstEvent2: arr[2].data["restaurant"]
      });
    });
  };
  
  console.log(event)

  useEffect(() => {
    setTimeout(getData, 3000)
  }, [event])


  return (
    <Event events={event} />
  );
}

export default API