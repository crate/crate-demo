package io.crate.demo

import java.io.{File, PrintWriter}
import java.util.concurrent.{ConcurrentHashMap, TimeUnit, ExecutorService, Executors}

import akka.actor._
import akka.util.Timeout

import io.crate.demo.common.Page
import io.crate.demo.parsers.WETParser

import scala.concurrent.Await
import akka.pattern.ask

import scala.concurrent.duration._

import scala.io.Source
import argonaut._, Argonaut._
import io.crate.demo.printers.JsonCodecs._


class PageJSONWriterActor(outFile: File) extends Actor {

  val writer = new PrintWriter(outFile)
  var count = 0

  def receive = {
    case p: Page => writer.println(p.asJson); count += 1
    case j: Json => writer.println(j); count += 1
    case s: String => writer.println(s.asJson); count += 1
    case _ => println("this is strange")
  }

  override def postStop() = {
    writer.flush()
    writer.close()
    println(s"$count documents processed")
  }
}


object CCPreprocessor {
  val pool: ExecutorService = Executors.newFixedThreadPool(100)


  def main(args: Array[String]): Unit = {
    val t0 = System.nanoTime()
    preprocess(args(0), args.drop(1).toVector)
    val t1 = System.nanoTime()
    println(s"Elapsed time: ${(t1 - t0) / 1000000000.0}s")
  }

  def preprocess(resultFileName: String, sourceFileNames: Vector[String]) = {
    val system = ActorSystem("WriterSystem")
    val writer = system.actorOf(Props(new PageJSONWriterActor(new File(resultFileName))), name = "writer")

    println(s"processing ${sourceFileNames.length} files")
    val dnsCache = new ConcurrentHashMap[String, Option[String]]()
    sourceFileNames.foreach(sourceFileName => {
      val p = new WETParser {
        override val source: Source = Source.fromFile(sourceFileName)
        override val resolverCache = dnsCache
      }
      val allItems = p //.toVector.par


      for {f <- allItems}  {
        pool.execute(new Runnable {
          override def run(): Unit = {writer ! f.get().asJson}
        })
      }
    })
    pool.shutdown()
    println("Waiting ...")
    pool.awaitTermination(100, TimeUnit.DAYS)
    println("Pool terminated")

    implicit val timeout = Timeout(5 days)
    Await.ready(writer ? PoisonPill, Duration.Inf)

    system.terminate()
    Await.result(system.whenTerminated, Duration.Inf)
  }

}

