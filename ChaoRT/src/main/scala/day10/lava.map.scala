import scala.annotation.tailrec
import scala.util.matching.Regex
import scala.io.Source

enum Direction(x:Int,y:Int):
  val dx: Int = x
  val dy: Int = y

  case N extends Direction(0, -1)
  case E extends Direction(1, 0)
  case S extends Direction(0, 1)
  case O extends Direction(-1, 0)

  def rot90H():Direction =
    this match
      case Direction.N => Direction.E
      case Direction.E => Direction.S
      case Direction.S => Direction.O
      case Direction.O => Direction.N

end Direction

case class Point(x: Int, y: Int)

class Day10 extends Puzzle {
  def name: String = "day10"

  val sample =
    """89010123
      |78121874
      |87430965
      |96549874
      |45678903
      |32019012
      |01329801
      |10456732""".stripMargin.split("\\r?\\n").iterator

  def Puzzle1(l: Iterator[String]): Long =
    var map = TwoDMap(l.toIndexedSeq)
    map.allTailHead()

  def Puzzle2(l: Iterator[String]): Long =
    var map = TwoDMap(l.toIndexedSeq)
    map.allTailHeadPath()
}

case class TwoDMap(data:IndexedSeq[String]) {
  val width:Int = data.head.size
  val height:Int = data.size

  def next(p:Point, d:Direction): Option[Point] =
    val x = p.x+d.dx
    val y = p.y+d.dy
    if(x<0 || x >= width || y<0 || y >= height) then None
    else Some(Point(x,y))

  def value(p:Point): Char =
    data(p.y)(p.x)

  def update(p:Point, c:Char):TwoDMap =
    TwoDMap(data.updated(p.y, data(p.y).updated(p.x, c)))

  def display():String = data.mkString("","\r\n","")

  def risePoints(p:Point):List[Point] =
    val current:Int = value(p) - '0'
    println(current+":"+p)
    var res = List()
    // Iterate over enum values
    Direction.values.map(next(p,_)).collect { case Some(p) => p }.filter(value(_)-'0' == current+1).toList

  def trailheads(current:Int, target:Int, last:List[Point]): Int =
    if(last.size == 0 ) then 0
    else if(current == target) then last.size
    else trailheads(current+1, target, last.map(p => risePoints(p)).flatten.distinct)

  def trailheadsPaths(current:Int, target:Int, last:List[Point]): Int =
    if(last.size == 0 ) then 0
    else if(current == target) then last.size
    else trailheadsPaths(current+1, target, last.map(p => risePoints(p)).flatten)

  def searchAll(c:Char):List[Point] =
    (0 until height).map(y => (0 until width).map(x => Point(x,y)).toList ).flatMap(_.iterator).filter(value(_) == c).toList

  def allTailHead():Int =
    searchAll('0').map(p => trailheads(0, 9, List(p))).sum

  def allTailHeadPath():Int =
    searchAll('0').map(p => trailheadsPaths(0, 9, List(p))).sum

  def nextIs(p:Point, c:Char, d:Direction):Boolean =
    next(p, d) match
      case None => false
      case Some(p) => value(p) == c
}