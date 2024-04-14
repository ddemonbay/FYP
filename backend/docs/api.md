# API Doc

### Usage

1. Request a generateTopic and wait for a minute
2. Then you can get the curriculum and Prerequisites
3. All APIs are HTTP POST

***************************************************************************

### Authentication

Input ***Header*** for authorization (key, value) in HTTP POST Request:

`authorizationUserLoginToken | qwertyuiop:{username}`

e.g. `authorizationUserLoginToken | qwertyuiop:damon`

*********************************

`/tutorial`
https://ugymjg1tfk.execute-api.us-east-1.amazonaws.com/Implementation/tutorial/

*********************************

`/generateTopic`

Request:
```
body(raw): 
{
	"topic": "Linear Algebra"
}
```

Reponse:

Server reponse with the topic id for it

`"Topic ID:2"`

**************************************************************************

`/getPrerequisites`

Request:

```
body(raw):
{
	"topicId": "2"
}
```

Response:

Server reponse with the prerequisites dictionary

```
{
	"prerequisites": 
		{
			"Knowledge Requirements": "Basic understanding of mathematics and an interest in social sciences.",
			"Suggested Preparatory Material": "\"Principles of Economics\" by N. Gregory Mankiw, Khan Academy courses on macroeconomics and microeconomics."
		}
}
```

*************************************

`/getCurriculum`

Request:

```
body(raw):
{
	"topicId": "2"
}
```
  
Reponse:

Server reponse with the curriculum dictionary
{
	"curriculum": 
		{
			"1.1": "Foundations of Linear Algebra",
			"1.2": "Solving Systems of Linear Equations",
			"1.3": "Vector Spaces", 
			"1.4": "Linear Transformations",
			"1.5": "Eigenvalues and Eigenvectors",
			"1.6": "Applications and Case Studies in Linear Algebra",
			"1.7": "Advanced Topics and Current Innovations"
		}
}

*****************************************************

`/getTopicIdPair`

Request:

no input needed

Response:

```
{
	"topicIdPair":
		{
			"1": "Introduction to Psychology",
			"2": "Linear Algebra",
			"3": "maths",
			"4": "Introduction to Physics",
			"5": "Introduction to Economics"
		}
}
```

*****************************************************
/getChatHistory
Request:
	{
		"topicId":  "7",
		"courseNumber": "1.4"
	}
Reponse:
If have chat history
Array chatHistory[], items in chatHistory[] is subarray having [role, content]

```
{
	"chatHistory": [
		[
			"system",
			"Today, we will delve into Contemporary Issues in Architecture, focusing on sustainable design, the impact of technology, and architecture as a social practice. Our goal is to understand how these elements influence contemporary architectural practices and how we, as future architects, can incorporate these principles into our design projects.\n\n**Sustainable Design** is one of the most critical contemporary issues. It involves creating buildings and environments with minimal environmental impact by utilizing energy-efficient technologies, sustainable materials, and environmentally friendly construction practices. An example of sustainable design is using solar panels for energy, rainwater harvesting systems for water usage, and choosing materials that have a low carbon footprint. The Bullitt Center in Seattle, often dubbed as \"the greenest commercial building in the world,\" utilizes these principles by generating its own electricity and capturing and treating all of its water on-site.\n\								n**Digital Fabrication** represents the intersection of technology and architecture. It involves the use of digital technologies, like 3D printing and computerized cutting machines, to produce complex architectural forms and components. This technology allows for more precision, reduces waste, and offers new possibilities for design innovation. For instance, the ICD/ITKE Research Pavilion, created by the University of Stuttgart, demonstrates the potential of digital fabrication through its biomimetic architectural structures, inspired by natural forms and realized with cutting-edge computational design and robotic fabrication techniques.\n\n**Architecture as a Social Practice** emphasizes the role of architecture in addressing social issues and improving the quality of life for communities. This approach involves engaging with the community, understanding their needs, and designing spaces that are inclusive and responsive to those needs. The incremental housing project in Monterrey, Mexico, by ELEMENTA								L, is an excellent example. It focuses on providing affordable housing solutions that can grow and evolve over time according to the residents' needs and financial capabilities.\n\nFor your design project, I encourage you to incorporate sustainable design principles, explore the use of digital fabrication techniques, and consider the social impact of your architectural design. Think of ways your design can contribute positively to the environment, leverage the latest technology for innovative solutions, and address the needs of its users and the broader community.\n\nNow, to better understand these concepts, let's discuss how you might apply sustainable design principles in a project. Consider a community center you're tasked to design. How would you implement sustainable design elements to ensure the building is energy-efficient, uses sustainable materials, and positively impacts the local community? Feel free to share your thoughts or ask questions.\n\nFor those interested in further exploring these 								topics, I recommend the book \"Sustainable Design: A Critical Guide\" by David Bergman for deep insights into sustainable architecture practices.\n\n[If you want to continue the lesson, please enter \"continue.\"]"
		],
		[
			"user",
			"continue"
		]
	]
}
```

If no chathistory (which means having set up course yet)

Reponse:

"NoHistory"

*****************************************************

`/generateCourse`

wait around 40s
Start a new course, you need to generate course first inorder to use sendGptMsg

Request:

```
{
	"topicId":  "7",
	"courseNumber": "1.4"
}
```

Response:

"Generating Course"

*****************************************************

`/sendGptMsg`

wait around 40s

Request:

```
{
	"topicId":  "7",
	"courseNumber": "1.4",
	"newMsg": "Continue" 
}
```

Response:

"Processing"