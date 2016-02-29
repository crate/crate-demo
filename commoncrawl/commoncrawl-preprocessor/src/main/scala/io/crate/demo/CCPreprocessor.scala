package io.crate.demo

import scala.collection.mutable.ListBuffer

import scala.io.Source
import upickle.default._


case class Page(uri: String, domain: String, reverseDomain: String, date: String, contentType: String, contentLength: Long, content: String)


trait WETParser extends Iterator[Page] {
  val _NL = "\r\n"

  val source: Source

  lazy val linesIterator = source.getLines()

  val blockDelimiter = "WARC/1.0"

  val metaData = ""

  private def valueOf(src: String) = src.splitAt(src.indexOf(':') + 1)._2.trim

  private def nextUntil(f: String => Boolean): Option[String] = {
    while (linesIterator.hasNext) {
      val current = linesIterator.next()
      if (f(current)) return Option(current)
    }
    return None
  }

  private def getUntil(f: String => Boolean): String = {
    val result = new ListBuffer[String]()
    while (linesIterator.hasNext) {
      val current = linesIterator.next()
      if (f(current)) return result.mkString(_NL)
      result append current
    }
    return result.mkString(_NL)
  }


  private def parseOne(): Option[Page] = {
    while (hasNext) {
      val warcType = valueOf(nextUntil(_ != blockDelimiter).get)

      if (warcType.compareToIgnoreCase("conversion") == 0) {
        val uri = valueOf(nextUntil(_.startsWith("WARC-Target-URI:")).get)
        val zonedDate = valueOf(nextUntil(_.startsWith("WARC-Date:")).get)
        val contentType = valueOf(nextUntil(_.startsWith("Content-Type:")).get)
        val contentLength = valueOf(nextUntil(_.startsWith("Content-Length:")).get).toLong
        linesIterator.next()

        val content = getUntil(_ == blockDelimiter)
        val domain = uri.split('/')(2)
        val reverseDomain = domain.split('.').reverse.mkString(".")

        return Option(new Page(uri, domain, reverseDomain, zonedDate, contentType, contentLength, content))
      }
    }
    return Option.empty
  }

  override def hasNext: Boolean = linesIterator.hasNext

  override def next(): Page = parseOne().getOrElse({
    source.close()
    throw new Exception("No more items")
  })

  def all = this.toVector
}


object CCPreprocessor {

  def main(args: Array[String]): Unit = {
    val sourceFileName = args(0)

    val p = new WETParser {
      override val source: Source = Source.fromFile(sourceFileName)
    }

    val allItems = p
    allItems.foreach(p => println(write(p)))
  }
}

