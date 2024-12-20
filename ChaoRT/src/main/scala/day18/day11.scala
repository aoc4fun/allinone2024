import scala.annotation.tailrec
import scala.util.matching.Regex
import scala.io.Source

case class Point(x: Int, y: Int)

class Day14 extends Puzzle {
  def name: String = "day14"

  val sample =
    """""".stripMargin.split("\\r?\\n").iterator

  def Puzzle1(l: Iterator[String]): Long = 0

  def Puzzle2(l: Iterator[String]): Long = 0
}