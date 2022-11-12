import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://kafka.canadacentral.cloudapp.azure.com:8100/stats`)
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
							<th>Tennis Court Bookings</th>
							<th>Tennis Lesson Bookings</th>
						</tr>
						<tr>
							<td># BP: {stats['num_court_bookings']}</td>
							<td># HR: {stats['num_lesson_bookings']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Court Bookings: {stats['max_court_bookings']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Lesson Bookings: {stats['max_lesson_bookings']}</td>
						</tr>
					
					</tbody>
                </table>
                <h3>Last Updated: {stats['current_timestamp']}</h3>

            </div>
        )
    }
}
