const your_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BTUkwiLCJzdWIiOiJDQzZYUk0iLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNzYzNTY1Njc3LCJpYXQiOjE3MzIwMjk2Nzd9.cvepX3vu6damhlWV9WdSU0FMaMJ7oInLYuGNEDSb8qw";
const access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BTUkwiLCJzdWIiOiJDQzZYUk0iLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNzYzNTY1Njc3LCJpYXQiOjE3MzIwMjk2Nzd9.cvepX3vu6damhlWV9WdSU0FMaMJ7oInLYuGNEDSb8qw";

//基本資料
fetch('https://api.fitbit.com/1/user/-/profile.json', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + your_access_token
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    console.log(data);
    const user = data.user;
    document.getElementById("displayName").innerHTML = user.displayName;
    document.getElementById("dateOfBirth").innerHTML = user.dateOfBirth;
    document.getElementById("gender").innerHTML = user.gender;
    document.getElementById("height").innerHTML = user.height;
    document.getElementById("weight").innerHTML = user.weight;
    document.getElementById("age").innerHTML = user.age;
    document.getElementById("languageLocale").innerHTML = user.languageLocale;
    document.getElementById("timezone").innerHTML = user.timezone;
})
.catch(error => {   // 錯誤處理，顯示錯誤訊息在主控台
    console.error('Error fetching data:', error);
    alert('Error fetching data. Please try again later.');
});

//心率
fetch('https://api.fitbit.com/1/user/-/activities/heart/date/2024-10-30/1d/1min/time/14%3A40/16%3A00.json', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + access_token
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    console.log(data);
    const heartData = data['activities-heart-intraday'].dataset;

    // 轉換數據為兩個陣列，一個是時間，一個是對應的心率
    const times = heartData.map(entry => entry.time);
    const heartRates = heartData.map(entry => entry.value);

    // 繪製心率折線圖
    const ctx = document.getElementById('heartRateChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: times, // x 軸為時間
            datasets: [{
                label: 'Heart Rate',  // 標籤名稱
                data: heartRates,  // y 軸為心率數據
                borderColor: 'rgba(75, 192, 192, 1)',  // 線條顏色
                backgroundColor: 'rgba(75, 192, 192, 0.2)',  // 填充顏色
                borderWidth: 2,  // 線條寬度
                fill: true,
                tension: 0.1  // 平滑曲線
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Heart Rate (BPM)'
                    },
                    suggestedMin: 50,// 最小心率顯示值
                    suggestedMax: 110// 最大心率顯示值
                }
            }
        }
    });
})
.catch(error => {
    console.error('Error fetching data:', error);
    alert('Error fetching heart rate data. Please try again later.');
});


