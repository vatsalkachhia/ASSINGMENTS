### Example 1: Informal & Brief

**Invitation:**
"Hey team, quick reminder about the project sync-up on 2025-09-25. Let's meet at 3:00 PM. Don't be late\!"

**Structured Invitation:**

```json
{
  "title": "project sync-up",
  "date": "2025-09-25",
  "time": "03:00 PM",
  "location": "",
  "attendees": ""
}
```

-----

### Example 2: Semi-Formal Email

**Invitation:**
"Hi everyone, Please join us for the weekly Sprint Planning Session. We'll meet next Friday, September 19, 2025, in the Main Boardroom. We'll kick things off at 11:00 AM sharp. We'll need Mike R. and Sarah L. to present their findings."

**Structured Invitation:**

```json
{
  "title": "Sprint Planning Session",
  "date": "2025-09-19",
  "time": "11:00 AM",
  "location": "Main Boardroom",
  "attendees": ["Mike R.", "Sarah L."]
}
```

-----

### Example 3: Very Formal Invitation

**Invitation:**
"Your presence is cordially requested at the Annual Charity Gala. The event will be held on the evening of October 4, 2025, commencing at eight o'clock, at The Grand Plaza Hotel."

**Structured Invitation:**

```json
{
  "title": "Annual Charity Gala",
  "date": "2025-10-04",
  "time": "08:00 PM",
  "location": "The Grand Plaza Hotel",
  "attendees": ""
}
```

-----

### Example 4: Casual & Conversational

**Invitation:**
"Just confirming our Team Lunch for tomorrow! Let's meet at the downtown cafe at 1:15 PM. I've already told Arjun and Sneha to be there."

**Structured Invitation:**

```json
{
  "title": "Team Lunch",
  "date": "2025-09-14",
  "time": "01:15 PM",
  "location": "downtown cafe",
  "attendees": ["Arjun", "Sneha"]
}
```

-----

### Example 5: Structured with Bullet Points

Invitation:
"Here are the details for our upcoming brainstorm:

  - What: Content Strategy Brainstorm
  - When: Monday, Sept 22nd at 2:30 in the afternoon
  - Where: The Nest (Breakout Room 4)
  - Who: Marketing Leads"

**Structured Invitation:**

```json
{
  "title": "Content Strategy Brainstorm",
  "date": "2025-09-22",
  "time": "02:30 PM",
  "location": "The Nest (Breakout Room 4)",
  "attendees": ["Marketing Leads"]
}
```

-----

### Example 6: Embedded Information (24-hour format)

Invitation:
"This email serves as a calendar invitation for the Client Kick-off Meeting scheduled for 2025-10-01 at 14:00. The meeting will be held virtually via the main company video link. Required attendees are the project lead and the design team head."

**Structured Invitation:**

```json
{
  "title": "Client Kick-off Meeting",
  "date": "2025-10-01",
  "time": "02:00 PM",
  "location": "Virtual via the main company video link",
  "attendees": ["project lead", "design team head"]
}
```