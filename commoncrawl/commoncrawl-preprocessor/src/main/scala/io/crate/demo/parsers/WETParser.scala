package io.crate.demo.parsers

import java.net.{Inet4Address, URI, InetAddress}
import java.time.ZonedDateTime
import java.util.concurrent.{ConcurrentMap, ConcurrentHashMap}

import io.crate.demo.common.Page

import scala.collection.mutable.ListBuffer
import scala.io.Source

trait PageProxy {
  def get(): Page
}

/**
  * Parses CommonCrawl's WET files.
  */
trait WETParser extends Iterator[PageProxy] {
  val _NL = "\r\n"


  val resolverCache: ConcurrentMap[String, Option[String]]

  class WETPageProxy(uri: String, zonedDate: ZonedDateTime, contentType: String, contentLength: Long, content: String) extends PageProxy {

    def get(): Page = Page(uri, tryResolve(uri), zonedDate, contentType, contentLength, content)
  }

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


  def tryResolve(uri: String): Option[String] = {
    val hostname = new URI(uri).getHost

    if (!resolverCache.containsKey(hostname)) {
      try {
        val address = Option(InetAddress.getByName(hostname).getHostAddress)
        resolverCache.put(hostname, address)
      } catch {
        case _: Throwable => resolverCache.put(hostname, None); return None
      }
    }
    resolverCache.get(hostname)
  }

  private def parseOne(): Option[PageProxy] = {
    while (hasNext) {
      val warcType = valueOf(nextUntil(_ != blockDelimiter).get)

      if (warcType.compareToIgnoreCase("conversion") == 0) {
        val uri = valueOf(nextUntil(_.startsWith("WARC-Target-URI:")).get)
        val zonedDate = ZonedDateTime.parse(valueOf(nextUntil(_.startsWith("WARC-Date:")).get))
        val contentType = valueOf(nextUntil(_.startsWith("Content-Type:")).get)
        val contentLength = valueOf(nextUntil(_.startsWith("Content-Length:")).get).toLong
        linesIterator.next()

        val content = getUntil(_ == blockDelimiter)
        return Option(new WETPageProxy(uri, zonedDate, contentType, contentLength, content))
      }
    }
    return Option.empty
  }

  override def hasNext: Boolean = linesIterator.hasNext

  override def next(): PageProxy = parseOne().getOrElse(throw new Exception("Cannot read source"))

  def all = this.toVector
}
