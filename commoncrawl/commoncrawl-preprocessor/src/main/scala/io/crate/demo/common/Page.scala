package io.crate.demo.common

import java.time.ZonedDateTime

case class Page(uri: String, ip: Option[String], date: ZonedDateTime, contentType: String, contentLength: Long, content: String)
