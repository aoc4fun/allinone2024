import scala.annotation.tailrec
import scala.util.matching.Regex
import scala.io.Source


class Day3 extends Puzzle:
  def name:String = "day3"
  val mulPattern: Regex = """^mul\(([0-9]+),([0-9]+)\)(.*)$""".r
  val doPattern: Regex = """^do\(\)(.*)$""".r
  val dontPattern: Regex = """^don't\(\)(.*)$""".r

  val test = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
  val test2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

  @tailrec
  private final def parseAndAdd(current: Long, s: String): Long =
    s match
      case "" => current
      case mulPattern(a, b, rest) => parseAndAdd(current + (a.toLong * b.toLong), rest)
      case _ => parseAndAdd(current, s.drop(1))

  @tailrec
  private final def parseAndAdd2(enabled: Boolean, current: Long, s: String): Long =
    s match
      case "" => current
      case mulPattern(a, b, rest) => parseAndAdd2(enabled, current + (if enabled then a.toLong * b.toLong else 0), rest)
      case doPattern(rest) => parseAndAdd2(true, current, rest)
      case dontPattern(rest) => parseAndAdd2(false, current, rest)
      case _ => parseAndAdd2(enabled, current, s.drop(1))

  def Puzzle1(l: Iterator[String]): Long = l.map(parseAndAdd(0, _)).sum
  def Puzzle2(l: Iterator[String]): Long = parseAndAdd2(true, 0, l.mkString(""))
end Day3