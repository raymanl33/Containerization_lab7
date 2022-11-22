import React, { useEffect, useState } from 'react'
import '../App.css';

export default function HealthStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://kafka.canadacentral.cloudapp.azure.com:8120/health`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Health Check</th>
						</tr>
						<tr>
							<td>Audit</td>
                            <td>{stats['audit']}</td> 
						</tr>
                        <tr>
                            <td>Processing</td>
                            <td>{stats['processing']}</td>             
                        </tr>
                        <tr>
                            <td>Receiver</td>
                            <td>{stats['receiver']}</td>
                        </tr>
                        <tr>
                        <td>Storage</td>
                        <td>{stats['storage']}</td>
                        </tr>

					</tbody>
                </table>
                <h3>Last Updated: {stats['Last_update']}</h3>

            </div>
        )
    }
}
