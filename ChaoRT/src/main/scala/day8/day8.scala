
case class Point(x: Int, y: Int) {
  infix def - (p2:Point) =
    Point(x-p2.x, y-p2.y)
  infix def +(p2: Point) =
    Point(x + p2.x, y + p2.y)

  infix def >(p2: Point) =
    p2+p2-this

}

case class TwoDMap(data:IndexedSeq[String]) {
  val width: Int = data.head.size
  val height: Int = data.size

  def value(p: Point): Char =
    data(p.y)(p.x)

  def update(p: Point, c: Char): TwoDMap =
    TwoDMap(data.updated(p.y, data(p.y).updated(p.x, c)))

  def display(): String =
    data.mkString("", "\r\n", "")

  def searchAll(c: Char): List[Point] =
    (0 until height).map(y => (0 until width).map(x => Point(x, y)).toList).flatMap(_.iterator).filter(value(_) == c).toList

  def distinctChars(): Set[Char] =
    val all = data.toList.map(_.distinct).mkString("")
    all.distinct.toSet

  def checkPoint(p: Point) =
    if (isValid(p)) then None
    else Some(p)
  def isValid(p:Point) =
    p.x >= 0 && p.x < width && p.y >= 0 && p.y < height
  def genAntiNode(p1: Point, p2: Point): List[Point] =
    List(p1 > p2, p2 > p1).filter(isValid).toList

  def genAllAntiNode(p1: Point, p2: Point): List[Point] =
    val step = p2-p1
    val p1p2 = LazyList.iterate(p2)(p => p + step).takeWhile(isValid).toList
    val p2p1 = LazyList.iterate(p1)(p=> p-step).takeWhile(isValid).toList
    p1p2++p2p1

}

class Day8 extends Puzzle {
  def name: String = "day8"

  val sample =
    """............
      |........0...
      |.....0......
      |.......0....
      |....0.......
      |......A.....
      |............
      |............
      |........A...
      |.........A..
      |............
      |............""".stripMargin.split("\\r?\\n").iterator


  def genAllAntinodesForFreq(antiNodeGenerator:(Point,Point)=>List[Point], freq:Char, orignal:TwoDMap, antinodes:TwoDMap):TwoDMap =
    var res = antinodes
    orignal.searchAll(freq).combinations(2).foreach( pair =>
      antiNodeGenerator(pair(0),pair(1)).foreach( p =>
        res = res.update(p, '#')
      )
    )
    res

  def antiNodesCount(antenasMap:TwoDMap, antiNodeGenerator:(Point,Point)=>List[Point]):Long =
    val freqs = antenasMap.distinctChars().filterNot(_ == '.').toList
    var antinodes = antenasMap
    freqs.foreach(f =>
      antinodes = genAllAntinodesForFreq(antiNodeGenerator, f, antenasMap, antinodes)
    )
    antinodes.searchAll('#').size

  def Puzzle1(l: Iterator[String]): Long =
    val antenasMap = TwoDMap(l.toIndexedSeq)
    antiNodesCount(antenasMap, antenasMap.genAntiNode)

  def Puzzle2(l: Iterator[String]): Long =
    val antenasMap = TwoDMap(l.toIndexedSeq)
    antiNodesCount(antenasMap, antenasMap.genAllAntiNode)

}