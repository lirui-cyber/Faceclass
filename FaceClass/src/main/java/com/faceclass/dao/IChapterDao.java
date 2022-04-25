package com.faceclass.dao;

import java.util.List;

import org.springframework.stereotype.Repository;

import com.faceclass.entity.Chapter;


@Repository("chapterDao")  
public interface IChapterDao {
	
	// 通过章节id 获得一个章节表 对象
	public Chapter getChapter(int chapterId);
	
	// 查询所有的章节表的数据
	public List<Chapter> selectAllChapter();
	
	// 通过课程id查找   章节表的集合   
	public List<Chapter> getAllChapterByCourseId(int courseId);
	
	// 通过课程id查找  包含小节列表的  章节表的数据
	public List<Chapter> getChapterAndSmallChapter(int courseId);	
	
	// 添加章节
	public int addChapter(Chapter chapter);
	
	// 删除章节
	public int deleteChapter(int chapterId);
	
	// 修改章节
	public int updateChapter(Chapter chapter);
}
