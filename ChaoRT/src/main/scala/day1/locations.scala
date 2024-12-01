import scala.math._
import scala.annotation.tailrec
import scala.io.Source
import scala.runtime.Statics

def convert(s:String):(Int,Int) = {
    val arr = s.split("[ ]+")
    (arr(0).toInt, arr(1).toInt)
}

def distance(tuple:(Int,Int)):Int = abs(tuple._2-tuple._1)

def countMap(l:List[Int]):Map[Int,Int]= l.groupBy(identity).mapValues(_.size).toMap

val sample1 ="""3   4
4   3
2   5
1   3
3   9
3   3
"""

val sampleAsList=sample1.split("\\r?\\n")

def puzzle1(l:Iterator[String]) = {
    val list = l.filter(_.size > 0).toList
    val lists = list.map(convert).unzip
    val l1 = lists(0).sorted
    val l2 = lists(1).sorted
    l1.zip(l2).map(distance).sum
}

def puzzle2(l:Iterator[String]) = {
    val list = l.filter(_.size > 0).toList
    val lists = list.map(convert).unzip
    val l1 = lists(0).sorted
    val map = countMap(lists(1))
    l1.map(i => i * map.getOrElse(i, 0)).sum
}

def puzzle1Full():Long =
    val lines = Source.fromFile("..\\..\\ressources\\day1.txt").getLines()
    puzzle1(lines)

def puzzle2Full():Long =
    val lines = Source.fromFile("..\\..\\ressources\\day1.txt").getLines()
    puzzle2(lines)
