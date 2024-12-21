import scala.annotation.tailrec
import scala.util.matching.Regex
import scala.io.Source


case class Point(x: Int, y: Int)

enum Direction(x:Int,y:Int):
  val dx: Int = x
  val dy: Int = y
  case N extends Direction(0, -1)
  case E extends Direction(1, 0)
  case S extends Direction(0, 1)
  case O extends Direction(-1, 0)

class Day20 extends Puzzle {
  def name: String = "day20"

  val sample =
    """###############
      |#...#...#.....#
      |#.#.#.#.#.###.#
      |#S#...#.#.#...#
      |#######.#.#.###
      |#######.#.#...#
      |#######.#.###.#
      |###..E#...#...#
      |###.#######.###
      |#...###...#...#
      |#.#####.#.###.#
      |#.#...#.#.#...#
      |#.#.#.#.#.#.###
      |#...#...#...###
      |###############""".stripMargin.split("\\r?\\n").iterator

  def Puzzle1(l: Iterator[String]): Long = {
    val map=TwoDMap(l.toIndexedSeq, Map())
    val indexedMap = map.indexSteps()
    indexedMap.allShortCuts().filter((p1,p2,p3) => indexedMap.calcGain(p1,p3) >=100).size
  }

  def Puzzle2(l: Iterator[String]): Long =
    val map=TwoDMap(l.toIndexedSeq, Map())
    val indexedMap = map.indexSteps()
    val trackPoints = indexedMap.searchAll('S') ++ indexedMap.searchAll('*').sortBy(p => -indexedMap.distanceToTargetOf(p)) ++ indexedMap.searchAll('E')
    val shortCuts = indexedMap.uniquePairs(trackPoints).filter(
      (p1,p2) => ((indexedMap.dist(p1,p2) <=20) && (indexedMap.calcGain(p1,p2) >=100)))
    shortCuts.size

  def countShortCutsGains() = {
    val map=TwoDMap(sample.toIndexedSeq, Map())
    val indexedMap = map.indexSteps()

    indexedMap.allShortCuts().groupBy(identity).view.mapValues(_.size).toMap
  }

  def countShortCutsGainsP2() = {
    val map=TwoDMap(sample.toIndexedSeq, Map())
    val indexedMap = map.indexSteps()

    val trackPoints = indexedMap.searchAll('S') ++ indexedMap.searchAll('*').sortBy(p => -indexedMap.distanceToTargetOf(p)) ++ indexedMap.searchAll('E')
    val shortCuts = indexedMap.uniquePairs(trackPoints).filter(
      (p1,p2) => ((indexedMap.dist(p1,p2) <=20) && (indexedMap.calcGain(p1,p2) >=50)))

    shortCuts.map((p1,p2) => indexedMap.calcGain(p1,p2)).groupBy(identity).view.mapValues(_.size).toMap
  }

  def showShortCuts() = {
    val map=TwoDMap(sample.toIndexedSeq, Map())
    val indexedMap = map.indexSteps()

    val shortCutStart = indexedMap.searchAll('S') ++ indexedMap.searchAll('*')

    val allShortCuts = shortCutStart.map(indexedMap.shortCuts(_)).flatten.toList
    var show = indexedMap
    allShortCuts
      .filter((p1,p2,p3) => indexedMap.calcGain(p1,p3) > 0)
      .foreach ((p1,p2,p3) => show=show.update(p2,'1').update(p3,'2'))

    show.display()
  }

}

case class TwoDMap(data:IndexedSeq[String], distanceToTarget:Map[Point,Int]) {
  val width: Int = data.head.size
  val height: Int = data.size


  def next(p:Point, d:Direction): Option[Point] =
    val x = p.x+d.dx
    val y = p.y+d.dy
    if(x<0 || x >= width || y<0 || y >= height) then None
    else Some(Point(x,y))

  def allShortCuts() = {
    val shortCutStart = searchAll('S') ++ searchAll('*')
    shortCutStart.map(shortCuts(_)).flatten.toList
  }

  def shortCuts(p:Point):List[(Point,Point,Point)] =
    Direction.values
      .map( d => (d, next(p, d)))
      .collect{ case (d, Some(pNext)) => (pNext, next(pNext, d)) }
      .collect{ case (p1,Some(p2)) if (value(p1) == '#') && ( value(p2) == '*' ||  value(p2) == 'E') => (p, p1, p2) }
      .filter((p1, p2, p3) => calcGain(p1,p3) > 0)
      .toList

  def calcGain(p1:Point, p2:Point) = distanceToTarget(p1)-distanceToTarget(p2) - dist(p1,p2)

  def value(p: Point): Char =
    data(p.y)(p.x)

  def update(p: Point, c: Char): TwoDMap =
    TwoDMap(data.updated(p.y, data(p.y).updated(p.x, c)), distanceToTarget)

  def updateDistance(p:Point, c:Char, i:Int):TwoDMap =
    TwoDMap(data.updated(p.y, data(p.y).updated(p.x, c)), distanceToTarget.updated(p,i))

  def distanceToTargetOf(p:Point) =
    val result = distanceToTarget.get(p).orElse(throw new IllegalArgumentException(s"not a track point ${p}"))
    result.get

  def dotAroundOrStart(p:Point):(Point,Char) = lookAround(p, '.', 'S' )

  def starAroundOrEnd(p:Point):(Point,Char) = lookAround(p, '*', 'E' )

  def lookAround(p:Point, search1:Char, search2: Char) =
    Direction.values.map(next(p, _))
      .collect{case Some(p) => (p, value(p))}
      .filter(tuple => tuple._2 == search1 || tuple._2 == search2)
      .head

  def indexSteps():TwoDMap = {
    def updateUntilFoundStart(last:Point, map: TwoDMap):TwoDMap = {
      if(value(last) == 'S') map
      else {
        val next = map.dotAroundOrStart(last)
        if (next._2 == 'S') map.updateDistance(next._1, 'S', map.distanceToTarget(last) + 1)
        else updateUntilFoundStart(next._1, map.updateDistance(next._1, '*', map.distanceToTarget(last) + 1))
      }
    }

    val start = searchAll('E')(0)
    val updated = updateDistance(start, 'E', 0)
    updateUntilFoundStart(start, updated)
  }

  def display(): String =
    data.mkString("", "\r\n", "")

  def printValue() =
    (0 until height).foreach(printLine(_))

  def printLine(y:Int) = {
    (0 until width).map(x => Point(x, y)).map(p => distanceToTarget.get(p) match {
      case None => print(s"  ${value(p)}")
      case Some(i) =>  print(s"  $i".takeRight(3))
    })
    println("")
  }

  def searchAll(c: Char): List[Point] =
    (0 until height).map(y => (0 until width).map(x => Point(x, y)).toList).flatMap(_.iterator).filter(value(_) == c).toList

  def isValid(p:Point) =
    p.x >= 0 && p.x < width && p.y >= 0 && p.y < height

  def dist(p1:Point, p2:Point):Int = math.abs(p1.x - p2.x)+math.abs(p1.y - p2.y)

  def uniquePairs(points: List[Point]) = for {
    (x, idxX) <- points.zipWithIndex
    (y, idxY) <- points.zipWithIndex
    if idxX < idxY
  } yield (x, y)
}

/**
 *
 * #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
 * # 82 81 80  # 74 73 72  # 58 57 56 55 54  #
 * # 83  # 79  # 75  # 71  # 59  #  #  # 53  #
 * # 84  # 78 77 76  # 70  # 60  # 50 51 52  #
 * #  #  #  #  #  #  # 69  # 61  # 49  #  #  #
 * #  #  #  #  #  #  # 68  # 62  # 48 47 46  #
 * #  #  #  #  #  #  # 67  # 63  #  #  # 45  #
 * #  #  #  2  1  0  # 66 65 64  # 42 43 44  #
 * #  #  #  3  #  #  #  #  #  #  # 41  #  #  #
 * #  6  5  4  #  #  # 24 25 26  # 40 39 38  #
 * #  7  #  #  #  #  # 23  # 27  #  #  # 37  #
 * #  8  # 14 15 16  # 22  # 28  # 34 35 36  #
 * #  9  # 13  # 17  # 21  # 29  # 33  #  #  #
 * # 10 11 12  # 18 19 20  # 30 31 32  #  #  #
 * #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
 *
 */
