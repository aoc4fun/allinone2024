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

  def update(p:Point, c:Char):TwoDMap =
    TwoDMap(data.updated(p.y, data(p.y).updated(p.x, c)))

  def newChar(p:Point, c:Char, d:Direction):Char =
    if(value(p) == '+') then '+'
    else if(value(p) == '*') then '*'
    else
      c match
        case '-' =>
          value(p) match
            case '^' | '|' => '+'
            case '\' => '\'
            case 'L' => 'L'
            case '/' => d match
              case Direction.E => '*'
            case 'J'
                => '*'

      case _ => '-'
        case '|' =>
          value(p) match
            case '-' => '+'
            case _ => '|'
  def draw(p:Point, c:Char):TwoDMap =
    update(p, newChar(p,c))

  def turnChar(d:Direction) =
    d match
      case N => '/'
      case E => '\'
      case S => 'J'
      case O => 'L'


  def display():String =
    data.mkString("","\r\n","")

  def searchAll(c:Char):List[Point] =
    (0 until height).map(y => (0 until width).map(x => Point(x,y)).toList ).flatMap(_.iterator).filter(value(_) == c).toList

  def nextIs(p:Point, c:Char, d:Direction):Boolean =
    next(p, d) match
      case None => false
      case Some(p) => value(p) == c
}

class Day6 extends Puzzle {
  def name: String = "day6"

  var sample =
    """....#.....
      |.........#
      |..........
      |..#.......
      |.......#..
      |..........
      |.#..^.....
      |........#.
      |#.........
      |......#...""".stripMargin.split("\\r?\\n").iterator

  def Puzzle1(l: Iterator[String]): Long = {
    var map = TwoDMap(l.toIndexedSeq)
    val start = map.searchAll('^').toList(0)
    var guard: Option[Guard] = Some(Guard(start, Direction.N, map))
    var last: Guard = guard.get
    while guard != None do {
      guard.get.nextPos() match
        case Some(g) => {
          guard = Some(g)
          last = g
        }
        case None => guard = None
    }
    map = last.map.update(last.pos, 'X')
    println(map.display())
    map.searchAll('X').size
  }

  def Puzzle2(l: Iterator[String]): Long = {
    var map = TwoDMap(l.toIndexedSeq)
    val start = map.searchAll('^').toList(0)
    (0 until map.width).map( x =>
      (0 until map.height).map( y =>
        val p = Point(x,y)
        map.value(p) match
          case '#'|'^' => 0
          case _ =>
            val updatedMap = map.update(p,'O')
            simPathAndCheckForLoop(updatedMap) match
              case SimulationEnd.Loop(last) =>
                1
              case _ => 0
      ).sum
    ).sum
  }

  def testOne() = {
    var map = TwoDMap(sample.toIndexedSeq)
    simPathAndCheckForLoop(map.update(Point(3,6), '#'))
  }

  def simPathAndCheckForLoop(map: TwoDMap): SimulationEnd = {
    val start = map.searchAll('^').toList(0)
    var g: Guard = Guard(start, Direction.N, map)
    var res = SimulationEnd.Run(g)

    while res match
      case SimulationEnd.Run(newG) =>
        g = newG
        true
      case _ => false
    do {
      res = g.simNext()
    }
    res
  }
}


case class Guard(pos:Point, d:Direction, map:TwoDMap, justTurned: Boolean = false) {
  def nextPos():Option[Guard] = {
    map.next(pos, d) match
      case None => None
      case Some(nextP) => map.value(nextP) match
        case '#' => Some(Guard(pos, d.rot90H(), map))
        case _ => Some(Guard(nextP, d, map.update(pos, 'X')))
  }
  def simNext():SimulationEnd = {
    map.next(pos, d) match
      case None => SimulationEnd.Out(Guard(pos, d, map))
      case Some(nextP) => map.value(nextP) match
        case '#'|'O' => if(justTurned) then
          SimulationEnd.Out(Guard(pos, d, map)) // forbid uturn - not in spec
            else
          SimulationEnd.Run(Guard(pos, d.rot90H(), map.update(pos, '*'), true))
        case '^' | '|' => d match
          case Direction.N | Direction.S => SimulationEnd.Run(Guard(nextP, d, map.draw(pos, '|')))
          case Direction.E | Direction.O => SimulationEnd.Run(Guard(nextP, d, map.draw(pos, '-')))
        case '*' => SimulationEnd.Loop(Guard(nextP, d, map))
        case '+' => d match
          case Direction.N | Direction.S => SimulationEnd.Run(Guard(nextP, d, map.draw(pos, '|')))
          case Direction.E | Direction.O => SimulationEnd.Run(Guard(nextP, d, map.draw(pos, '-')))
        case '.' => d match
          case Direction.N | Direction.S => SimulationEnd.Run(Guard(nextP, d, map.draw(pos, '|')))
          case Direction.E | Direction.O => SimulationEnd.Run(Guard(nextP, d, map.draw(pos, '-')))
        case '-' => d match
          case Direction.N | Direction.S => SimulationEnd.Run(Guard(nextP, d, map.draw(pos, '|')))
          case Direction.E | Direction.O => SimulationEnd.Run(Guard(nextP, d, map.draw(pos, '-')))
  }
}

enum SimulationEnd {
  case Out(lastPos:Guard)
  case Loop(lastPos:Guard)
  case Run(newPos:Guard)
}