import scala.annotation.tailrec
import scala.util.matching.Regex
import scala.io.Source
import scala.util.matching.Regex

enum Direction(x:Int,y:Int):
  val dx: Int = x
  val dy: Int = y

  case N extends Direction(0, 1)
  case NE extends Direction(1, 1)
  case E extends Direction(1, 0)
  case SE extends Direction(1, -1)
  case S extends Direction(0, -1)
  case SO extends Direction(-1, -1)
  case O extends Direction(-1, 0)
  case NO extends Direction(-1, 1)
  def flip():Direction=
    this match
      case Direction.S => Direction.N
      case Direction.N => Direction.S
      case Direction.E => Direction.O
      case Direction.O => Direction.E
      case Direction.SE => Direction.NO
      case Direction.NO => Direction.SE
      case Direction.SO => Direction.NE
      case Direction.NE => Direction.SO


end Direction

val corners = List(Direction.NO,Direction.NE,Direction.SE,Direction.SO)

class Day4 extends Puzzle:
  def name:String = "day4"

  val sample="""MMMSXXMASM
               |MSAMXMSMSA
               |AMXSXMAAMM
               |MSAMASMSMX
               |XMASAMXAMM
               |XXAMMXXAMA
               |SMSMSASXSS
               |SAXAMASAAA
               |MAMMMXMMMM
               |MXMXAXMASX""".stripMargin.split("\\r?\\n").iterator

  def getMap(s:Iterator[String]):TwoDMap= TwoDMap(s.toIndexedSeq)

  def Puzzle1(l: Iterator[String]): Long = getMap(l).countXmas()
  def Puzzle2(l: Iterator[String]): Long = getMap(l).countCrossMas()
end Day4


val headTail: Regex = """^(.)(.*)$""".r

case class Point(x: Int, y: Int)

case class TwoDMap(data:IndexedSeq[String]) {
  val width:Int = data.head.size
  val height:Int = data.size

  def next(p:Point, d:Direction): Option[Point] =
    //val x = if((p.x+d.dx) == -1) then width -1 else (p.x+d.dx)%width
    //val y = if((p.y+d.dy) == -1) then height -1 else (p.y + d.dy) % height
    val x = p.x+d.dx
    val y = p.y+d.dy
    if(x<0 || x >= width || y<0 || y >= height) then None
    else Some(Point(x,y))

  def value(p:Point): Char =
    data(p.y)(p.x)

  def matchWord(start:Point,direction: Direction, word:String): Boolean = {
    word match
      case "" => println(s"$start,$direction");true
      case headTail(head, tail) => if(value(start) != head.head) then false else next(start, direction) match
        case Some(p) => matchWord(p, direction, tail)
        case None => tail.isEmpty
  }

  def matchCount(start:Point, word: String): Int = Direction.values.count(matchWord(start, _, word))

  def searchAll(c:Char):List[Point] =
    (0 until height).map(y => (0 until width).map(x => Point(x,y)).toList ).flatMap(_.iterator).filter(value(_) == c).toList

  def nextIs(p:Point, c:Char, d:Direction):Boolean =
    next(p, d) match
      case None => false
      case Some(p) => value(p) == c
  def isXmas(p:Point):Boolean =
    p match
      case Point(x , y) if x==0 || y==0 || x == width-1 || y == height -1 => false
      case _ => value(p) == 'A' && corners.filter(nextIs(p,'M',_))
        .count(d => nextIs(p, 'S',d.flip())) == 2
  def countXmas():Long =
    searchAll('X').map(matchCount(_,"XMAS")).sum

  def countCrossMas():Long =
    searchAll('A').count(isXmas)
}