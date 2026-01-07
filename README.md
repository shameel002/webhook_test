# webhook_test

# FastAPI Application

## Health Monitoring

This application uses [UptimeRobot](https://uptimerobot.com) to prevent the Render free tier service from sleeping and to monitor uptime.

**Login:** Use your GitHub account at [https://uptimerobot.com](https://uptimerobot.com)

### Health Check Endpoint

The application exposes a `/health` endpoint for monitoring:
```
https://your-app-name.onrender.com/health
```

**Response:**
```json
{
  "status": "ok"
}
```

UptimeRobot pings this endpoint every 5 minutes using the HEAD method to keep the service active 24/7.

---

**Note:** Check the UptimeRobot dashboard for uptime status and alerts.
