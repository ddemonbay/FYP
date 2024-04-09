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

`"Topic ID: 2"`

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
