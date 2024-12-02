import scala.math._
import scala.annotation.tailrec
import scala.io.Source
import scala.runtime.Statics


val sample1 ="""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
@tailrec
def safe(sign:Int, l:List[Int]):Boolean =
  l match
    case Nil => true
    case head::Nil => true
    case head::head2::tail => comply(sign, head, head2) && safe(sign, head2::tail)

def comply(sign: Int, a: Int, b: Int): Boolean = (Math.abs(b - a) > 0 && Math.abs(b - a) < 4) && ((sign ^ (b - a)) >= 0)

def safe(l:List[Int]):Boolean =
  l match
    case Nil => true
    case head::Nil => true
    case head::head2::tail => safe(head2-head, head::head2::tail)


def genWithout(i:Int, l:List[Int]):List[Int] =
  l match
    case Nil => Nil
    case head :: tail => if(i==0) then tail else head::genWithout(i-1, tail)

def possibleCorrecrLists(l:List[Int]):List[List[Int]] = {
  val item = 0 until l.size
  item.map(genWithout(_, l)).toList
}

def relaxedSafe(l:List[Int]):Boolean =
  safe(l) || possibleCorrecrLists(l).exists(safe(_))

def splitToList(s:String):List[Int] =
  s.split("[ ]+").map(_.toInt).toList


def puzzle1(l:List[String]):Int = puzzle1(l.iterator)
def puzzle1(l:Iterator[String]):Int = {
  l.map(splitToList).count(safe)
}
val sampleAsList=sample1.split("\\r?\\n").iterator

def puzzle2(l:Iterator[String]):Int = {
  l.map(splitToList).count(relaxedSafe)
}

def puzzle1Full():Long =
  val lines = Source.fromFile("..\\..\\ressources\\day2.txt").getLines()
  puzzle1(lines)

def puzzle2Full():Long =
  val lines = Source.fromFile("..\\..\\ressources\\day2.txt").getLines()
  puzzle2(lines)