name := "ccpp"

version := "1.0"

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  "org.scalatest" %% "scalatest" % "2.2.6" % "test",
  "io.argonaut" %% "argonaut" % "6.0.4",
  "com.typesafe.akka" %% "akka-actor" % "2.4.1"
)
// Uncomment to use Akka
//libraryDependencies += "com.typesafe.akka" %% "akka-actor" % "2.3.11"
