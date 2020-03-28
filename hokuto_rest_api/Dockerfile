FROM openjdk:8-alpine

COPY target/uberjar/hokuto_rest_api.jar /hokuto_rest_api/app.jar

EXPOSE 3000

CMD ["java", "-jar", "/hokuto_rest_api/app.jar"]
