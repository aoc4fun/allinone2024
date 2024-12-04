import scala.io.Source

trait Puzzle:
  lazy val lines:Iterator[String] = Source.fromFile(s"..\\..\\ressources\\$name.txt").getLines()

  def Puzzle1Full() = Puzzle1(lines)
  def Puzzle2Full() = Puzzle2(lines)

  def Puzzle1(l:List[String]): Long = Puzzle1(l.iterator)
  def Puzzle2(l:List[String]): Long = Puzzle2(l.iterator)

  def name:String
  def Puzzle1(l: Iterator[String]): Long
  def Puzzle2(l: Iterator[String]): Long
end Puzzle
