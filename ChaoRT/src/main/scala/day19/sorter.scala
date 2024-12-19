import scala.annotation.tailrec
import scala.util.matching.Regex
import scala.io.Source

case class Point(x: Int, y: Int)

class Day19 extends Puzzle {
  def name: String = "day19"

  val sample =
    """r, wr, b, g, bwu, rb, gb, br
      |
      |brwrr
      |bggr
      |gbbr
      |rrbgbr
      |ubwu
      |bwurrg
      |brgr
      |bbrgwb""".stripMargin.split("\\r?\\n").iterator

  def Puzzle1(l: Iterator[String]): Long = {
    val choices = parseChoiceList(l)
    val targets = parseTarget(l)
    targets.foreach(s => println(s"$s: ${possibleSolutionFor(s, choices)}"))
    targets.map(possibleSolutionFor(_, choices)).count(_ > 0)
  }

  def Puzzle2(l: Iterator[String]): Long =  {
    val choices = parseChoiceList(l)
    val targets = parseTarget(l)
    targets.map(possibleSolutionFor(_, choices)).sum
  }

  def possibleSolutionFor(target:String, choices:List[String]):Long =
    var endMatchPerIndex = List.fill(target.length + 1)(0L)
    endMatchPerIndex=endMatchPerIndex.updated(0,1)
    (1 to target.length).foreach(i => choices.foreach(choice =>
      endMatchPerIndex = updateIfMatch(endMatchPerIndex, target, choice, i)
    ))
    endMatchPerIndex(target.length)

  def updateIfMatch(endMatcherCount:List[Long], s:String, toTest:String, index: Int):List[Long] =
    if(index < toTest.length) then endMatcherCount
    else {
      val tested = s.substring(index-toTest.length, index)
      if(tested.equals(toTest)) then
        endMatcherCount.updated(index, endMatcherCount(index) + endMatcherCount(index - toTest.length))
      else endMatcherCount
    }

  def parseChoiceList(l:Iterator[String]):List[String] = {
    val line = l.next()
    line.split("\\,\\s").toList
  }


  def parseTarget(l:Iterator[String]):List[String] =
    l.next()
    l.toList

  def someCanEnd(s:String, choices:Map[Char,Array[String]]) =
    choices.exists((k,v) => v.exists(possible => s.endsWith(possible)))
  def someCanStart(s:String, choices:Map[Char,Array[String]]) =
    choices.exists((k,v) => v.exists(possible => s.startsWith(possible)))


  def canMatch(s:String, choices:Map[Char,Array[String]]):Boolean = {
    if (!someCanStart(s,choices) || !someCanEnd(s, choices)) then false
    else s match
      case "" => true
      case _ => choices.get(s.head) match
        case None => false
        case Some(possibleChoice) => possibleChoice
            .filter(s.startsWith(_))
            .find(choice => canMatch(s.substring(choice.length), choices)).isDefined
  }
}

// ugbbggburwguwbgugwbbgbbwgrgguwbgrrwwwwugrbrgwwrguggbrurgrggr
