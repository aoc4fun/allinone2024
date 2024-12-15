import scala.annotation.tailrec
import scala.util.matching.Regex
import scala.io.Source

class Day14 extends Puzzle {
  def name: String = "day14"

  val sample =
    """p=0,4 v=3,-3
      |p=6,3 v=-1,-3
      |p=10,3 v=-1,2
      |p=2,0 v=2,-1
      |p=0,0 v=1,3
      |p=3,0 v=-2,-2
      |p=7,6 v=-1,-3
      |p=3,0 v=-1,-2
      |p=9,3 v=2,3
      |p=7,3 v=-1,2
      |p=2,4 v=2,-3
      |p=9,5 v=-3,-3""".stripMargin.split("\\r?\\n").iterator

  def Puzzle1(l: Iterator[String]): Long = {
    val r = Restroom(101,103)
    var qad = Quadrant(r)
    parseInitial(l,r)
      .map(_.move(100))
      .foreach( rob =>
        qad = qad.update(rob)
      )
    qad.safetyFactor()
  }

  def Puzzle2(l: Iterator[String]): Long =
    val r = Restroom(101,103)
    val robots = parseInitial(l,r)
    var index=0
    while(!isTree(robots.map(_.move(index)))) {
      index=index+1
    }
    index

  def isTree(l:List[Robot]) = {
    val size = l.size
    l.map(_.initalPos).distinct.size == size
  }


  def parseInitial(s: Iterator[String], r:Restroom): List[Robot] = {
    s.map(
      parseOne(_,r)
    ).toList
  }
  val robotDef: Regex = """^p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)$""".r

  def parseOne(s:String, r:Restroom) : Robot =
    s match
      case robotDef(px,py,vx,vy) => Robot(Point(px.toInt,py.toInt), Velocity(vx.toInt,vy.toInt), r)

  def test() = {
    val r = Restroom(11,7)
    var qad = Quadrant(r)
    parseInitial(sample,r)
      .map(_.move(100))
      .foreach( rob =>
        qad = qad.update(rob)
      )
    qad.safetyFactor()
  }


}

case class Restroom(width:Int, height: Int)
case class Point(x:Int, y:Int)
case class Velocity(x:Int, y:Int)
case class Robot(initalPos:Point, v:Velocity, r:Restroom) {
  def move(count:Int) : Robot = {
    val x = (initalPos.x+v.x*count)%r.width
    val y = (initalPos.y+v.y*count)%r.height
    Robot(Point(if( x < 0 ) then (x + r.width) else x,
      if( y < 0 ) then (y + r.height) else y), v,r)
  }
  def x():Int = this.initalPos.x
  def y():Int = this.initalPos.y

}

case class Quadrant(r:Restroom, q1:Int=0, q2:Int=0, q3:Int=0, q4:Int=0) {
  val splitX = r.width/2
  val splity = r.height/2

  def update(robot: Robot) : Quadrant =
    if(robot.x() < splitX) then
      if(robot.y() < splity) then Quadrant(r, q1+1, q2,q3,q4)
      else if(robot.y() > splity) then Quadrant(r, q1, q2,q3+1,q4)
      else this
    else if(robot.x() > splitX) then
     if(robot.y() < splity) then Quadrant(r, q1, q2+1,q3,q4)
     else if(robot.y() > splity) then Quadrant(r, q1, q2,q3,q4+1)
     else this
    else this

  def safetyFactor():Int = q1*q2*q3*q4
}